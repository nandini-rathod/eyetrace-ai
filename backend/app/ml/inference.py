"""
EyeTrace AI — Inference Pipeline
Replicates exact preprocessing and feature extraction from ASD_EyeTracking_Pipeline.ipynb:
  1. Load image as RGB
  2. Resize to 224x224
  3. Gaussian blur (kernel 5x5, sigma=0)
  4. Min-Max normalization to [0, 1]: (img - min) / (max - min + 1e-8)
  5. Scale to [0, 255] uint8 -> float32 -> MobileNet preprocess_input (scales to [-1, 1])
  6. MobileNet feature extraction with pooling='avg' -> 1024-dim
  7. PCA transform (250 components) -> 250-dim
  8. StackingClassifier predict + predict_proba
     Classes: 0 = Non-ASD, 1 = ASD
"""
import io
import logging
import numpy as np
import cv2
from PIL import Image

logger = logging.getLogger(__name__)


def preprocess_image(image_bytes: bytes):
    """
    Replicates the exact notebook preprocessing pipeline.
    Returns (preprocessed_input [1,224,224,3], original_rgb_array [224,224,3])
    """
    from tensorflow.keras.applications.mobilenet import preprocess_input

    # 1. Load as RGB PIL image
    pil_img = Image.open(io.BytesIO(image_bytes)).convert("RGB")

    # 2. Resize to 224x224
    pil_img = pil_img.resize((224, 224), Image.LANCZOS)
    original_rgb = np.array(pil_img, dtype=np.uint8)  # for visualization

    # 3. Gaussian blur (kernel 5x5, sigma=0)
    img_float = original_rgb.astype(np.float32)
    img_blurred = cv2.GaussianBlur(img_float, (5, 5), 0)

    # 4. Min-Max normalization to [0, 1]
    img_min = img_blurred.min()
    img_max = img_blurred.max()
    img_norm = (img_blurred - img_min) / (img_max - img_min + 1e-8)

    # 5. Convert to [0, 255] uint8, then apply MobileNet preprocess_input
    img_uint8 = (img_norm * 255.0).astype(np.uint8)
    img_input = np.expand_dims(img_uint8.astype(np.float32), axis=0)
    img_preprocessed = preprocess_input(img_input)

    return img_preprocessed, original_rgb


def extract_features(mobilenet_model, img_preprocessed: np.ndarray) -> np.ndarray:
    """
    Run MobileNet with pooling='avg' to get 1024-dim feature vector.
    Returns shape (1, 1024).
    """
    features = mobilenet_model.predict(img_preprocessed, verbose=0)
    logger.debug(f"MobileNet features shape: {features.shape}")
    return features


def run_inference(mobilenet_model, pca, stacking_clf, image_bytes: bytes) -> dict:
    """
    Full inference pipeline. Returns dict with prediction, score, probabilities.
    Notebook class labels:
      0 = Non-ASD (Non_Autistic)
      1 = ASD (Autistic)
    """
    # Preprocess
    img_preprocessed, original_rgb = preprocess_image(image_bytes)

    # Feature extraction
    features = extract_features(mobilenet_model, img_preprocessed)  # (1, 1024)

    # PCA transform — do NOT refit
    features_pca = pca.transform(features)  # (1, 250)
    logger.debug(f"PCA features shape: {features_pca.shape}")

    # Classifier
    prediction_raw = stacking_clf.predict(features_pca)[0]
    proba = stacking_clf.predict_proba(features_pca)[0]  # [p_class_0, p_class_1]

    classes = list(stacking_clf.classes_)
    logger.debug(f"Classifier classes: {classes}, prediction: {prediction_raw}, proba: {proba}")

    # Find index of ASD (1) and Non-ASD (0)
    # The notebook explicitly mapped: 1 -> ASD, 0 -> Non-ASD
    asd_class_idx = 1 if 1 in classes else 0
    non_asd_class_idx = 0 if 0 in classes else (1 - asd_class_idx)

    # Identify whether prediction is ASD
    predicted_label = "ASD" if int(prediction_raw) == 1 else "Non-ASD"

    asd_score = float(proba[asd_class_idx])
    non_asd_score = float(proba[non_asd_class_idx])
    confidence = float(proba.max())

    return {
        "predicted_label": predicted_label,
        "confidence": confidence,
        "asd_probability": asd_score,
        "non_asd_probability": non_asd_score,
        "raw_prediction": int(prediction_raw),
        "original_rgb": original_rgb,
        "features_pca": features_pca,
    }
