"""
EyeTrace AI — Explainability Utilities (Vectorized & Fast)

Implements mathematically valid explainability for the pipeline:
  MobileNet feature extraction -> PCA -> StackingClassifier

Methods used:
  1. Occlusion Sensitivity — patch-based image perturbation (vectorized batching)
  2. Channel Ablation    — zero out individual RGB channels (vectorized batching)
  3. RGB Channel Visualization — per-channel colored images

Note: Grad-CAM is NOT used because the final classifier is sklearn-based
(StackingClassifier), which breaks the gradient graph. Occlusion sensitivity
is model-agnostic and valid for any pipeline.
"""
import io
import base64
import logging
import numpy as np
import cv2
from PIL import Image

logger = logging.getLogger(__name__)


def _ndarray_to_base64_png(arr: np.ndarray) -> str:
    """Convert a uint8 numpy array (H,W) or (H,W,3) to base64-encoded PNG."""
    if arr.ndim == 2:
        pil = Image.fromarray(arr.astype(np.uint8), mode="L")
    else:
        pil = Image.fromarray(arr.astype(np.uint8), mode="RGB")
    buf = io.BytesIO()
    pil.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode("utf-8")


def _prepare_image_for_model(img_rgb: np.ndarray):
    """Applies exact blur, min-max norm, and mobilenet preprocessing."""
    from tensorflow.keras.applications.mobilenet import preprocess_input

    img_float = img_rgb.astype(np.float32)
    img_blurred = cv2.GaussianBlur(img_float, (5, 5), 0)
    img_min = img_blurred.min()
    img_max = img_blurred.max()
    img_norm = (img_blurred - img_min) / (img_max - img_min + 1e-8)
    img_uint8 = (img_norm * 255.0).astype(np.uint8)
    return preprocess_input(np.expand_dims(img_uint8.astype(np.float32), 0))


def compute_occlusion_heatmap(
    mobilenet_model,
    pca,
    stacking_clf,
    original_rgb: np.ndarray,
    asd_class_idx: int = 1,
    patch_size: int = 32,
    stride: int = 32,
) -> str:
    """
    Occlusion sensitivity: slide a neutral patch over the image, re-run inference
    in micro-batches to strictly respect free-tier memory constraints (512MB RAM).
    """
    import gc

    H, W = original_rgb.shape[:2]
    score_map = np.zeros((H, W), dtype=np.float32)
    count_map = np.zeros((H, W), dtype=np.float32)

    # Baseline score (no occlusion)
    base_input = _prepare_image_for_model(original_rgb)
    base_features = mobilenet_model(base_input, training=False).numpy()
    base_pca = pca.transform(base_features)
    base_proba = stacking_clf.predict_proba(base_pca)[0][asd_class_idx]

    gray_fill = np.array([128, 128, 128], dtype=np.uint8)

    patches_coords = []
    occ_inputs = []

    for y in range(0, H - patch_size + 1, stride):
        for x in range(0, W - patch_size + 1, stride):
            occluded = original_rgb.copy()
            occluded[y:y+patch_size, x:x+patch_size] = gray_fill
            patches_coords.append((y, x))
            occ_inputs.append(_prepare_image_for_model(occluded)[0])

    if occ_inputs:
        BATCH_SIZE = 16
        occ_features_list = []
        for i in range(0, len(occ_inputs), BATCH_SIZE):
            chunk = np.stack(occ_inputs[i:i+BATCH_SIZE], axis=0)
            chunk_feats = mobilenet_model(chunk, training=False).numpy()
            occ_features_list.append(chunk_feats)
        
        occ_features = np.vstack(occ_features_list)
        occ_pca = pca.transform(occ_features)
        occ_probas = stacking_clf.predict_proba(occ_pca)[:, asd_class_idx]

        for (y, x), occ_proba in zip(patches_coords, occ_probas):
            importance = base_proba - occ_proba
            score_map[y:y+patch_size, x:x+patch_size] += importance
            count_map[y:y+patch_size, x:x+patch_size] += 1
            
        del occ_inputs, occ_features_list, occ_features, occ_pca
        gc.collect()

    count_map = np.maximum(count_map, 1)
    heatmap = score_map / count_map

    # Normalize to 0-255
    hmin, hmax = heatmap.min(), heatmap.max()
    if hmax > hmin:
        heatmap_norm = ((heatmap - hmin) / (hmax - hmin) * 255).astype(np.uint8)
    else:
        heatmap_norm = np.zeros_like(heatmap, dtype=np.uint8)

    heatmap_color = cv2.applyColorMap(heatmap_norm, cv2.COLORMAP_JET)
    heatmap_rgb = cv2.cvtColor(heatmap_color, cv2.COLOR_BGR2RGB)
    overlay = cv2.addWeighted(original_rgb, 0.55, heatmap_rgb, 0.45, 0)

    return _ndarray_to_base64_png(overlay)


def compute_channel_ablation(
    mobilenet_model,
    pca,
    stacking_clf,
    original_rgb: np.ndarray,
    baseline_asd_proba: float,
    asd_class_idx: int = 1,
) -> dict:
    """
    Zero out one RGB channel at a time, batched across all 3 channels.
    """
    channel_names = {0: "Red (Velocity)", 1: "Green (Acceleration)", 2: "Blue (Jerk)"}
    ablated_inputs = []

    for ch_idx in range(3):
        ablated = original_rgb.copy()
        ablated[:, :, ch_idx] = 0
        ablated_inputs.append(_prepare_image_for_model(ablated)[0])

    ablated_batch = np.stack(ablated_inputs, axis=0)  # (3, 224, 224, 3)
    feats = mobilenet_model(ablated_batch, training=False).numpy()
    pca_feats = pca.transform(feats)
    probas = stacking_clf.predict_proba(pca_feats)[:, asd_class_idx]

    results = {}
    for ch_idx, ch_name in channel_names.items():
        proba = probas[ch_idx]
        delta = baseline_asd_proba - float(proba)
        results[ch_name] = {
            "baseline_asd_probability": round(baseline_asd_proba, 4),
            "ablated_asd_probability": round(float(proba), 4),
            "delta": round(delta, 4),
            "importance": round(abs(delta), 4),
            "direction": "supports Non-ASD class" if delta < 0 else "supports ASD class",
        }

    return results


def compute_rgb_channel_images(original_rgb: np.ndarray) -> dict:
    """
    Extract individual RGB channels as colormapped base64 PNG images.
    R = Velocity, G = Acceleration, B = Jerk
    """
    r_channel = original_rgb[:, :, 0]
    g_channel = original_rgb[:, :, 1]
    b_channel = original_rgb[:, :, 2]

    def channel_to_colored_b64(ch_array: np.ndarray, colormap: int) -> str:
        colored = cv2.applyColorMap(ch_array, colormap)
        colored_rgb = cv2.cvtColor(colored, cv2.COLOR_BGR2RGB)
        return _ndarray_to_base64_png(colored_rgb)

    return {
        "red_velocity": channel_to_colored_b64(r_channel, cv2.COLORMAP_HOT),
        "green_acceleration": channel_to_colored_b64(g_channel, cv2.COLORMAP_SUMMER),
        "blue_jerk": channel_to_colored_b64(b_channel, cv2.COLORMAP_COOL),
        "original": _ndarray_to_base64_png(original_rgb),
    }
