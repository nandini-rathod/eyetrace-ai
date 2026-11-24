"""Prediction endpoint — POST /api/v1/predict"""
import uuid
import logging
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse

from app.ml.model import get_state
from app.ml.inference import run_inference
from app.utils.explainability import (
    compute_occlusion_heatmap,
    compute_channel_ablation,
    compute_rgb_channel_images,
)
from app.schemas.prediction import (
    PredictionResponse,
    ExplainabilityResult,
    VisualizationsResult,
    ChannelAblationResult,
)

router = APIRouter()
logger = logging.getLogger(__name__)

ALLOWED_CONTENT_TYPES = {"image/png", "image/jpeg", "image/jpg"}
MAX_FILE_SIZE_BYTES = 10 * 1024 * 1024  # 10 MB

DISCLAIMER = (
    "This analysis is for academic research purposes only and must NOT be used "
    "as a clinical diagnostic tool. The model was trained on a limited dataset "
    "(219 ASD + 328 Non-ASD samples) and has not been validated for clinical use. "
    "ASD diagnosis requires comprehensive multidisciplinary clinical evaluation."
)


@router.post("/api/v1/predict")
async def predict(image: UploadFile = File(...)):
    state = get_state()

    # --- Validate model availability ---
    if not state.model_loaded:
        raise HTTPException(
            status_code=503,
            detail={
                "error": "Model not ready",
                "detail": (
                    "One or more model artifacts are unavailable. "
                    f"PCA: {'✅' if state.pca_available else '❌'}  "
                    f"StackingCLF: {'✅' if state.stacking_clf_available else '❌'}  "
                    f"MobileNet: {'✅' if state.mobilenet_available else '❌'}"
                ),
                "load_error": state.load_error,
            },
        )

    # --- Validate file type ---
    ct = (image.content_type or "").lower()
    if ct not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=415,
            detail=f"Unsupported file type '{ct}'. Only PNG, JPG, JPEG are accepted.",
        )

    # --- Read file ---
    image_bytes = await image.read()
    if len(image_bytes) == 0:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")
    if len(image_bytes) > MAX_FILE_SIZE_BYTES:
        raise HTTPException(
            status_code=413,
            detail=f"File too large ({len(image_bytes):,} bytes). Maximum is 10 MB.",
        )

    logger.info(f"Received image: {image.filename!r}, size={len(image_bytes):,} bytes")

    # --- Run inference ---
    try:
        result = run_inference(
            state.mobilenet_model,
            state.pca,
            state.stacking_clf,
            image_bytes,
        )
    except Exception as e:
        logger.exception("Inference error")
        raise HTTPException(status_code=500, detail=f"Inference failed: {e}")

    predicted_label = result["predicted_label"]
    asd_proba = result["asd_probability"]
    non_asd_proba = result["non_asd_probability"]
    confidence = result["confidence"]
    original_rgb = result["original_rgb"]

    # Determine ASD class index for explainability
    # The training notebook encoded: 0 = Non-ASD, 1 = ASD
    classes = list(state.stacking_clf.classes_)
    asd_class_idx = 1 if 1 in classes else 0

    # --- RGB Channel visualizations ---
    logger.info("Computing channel visualizations ...")
    channel_imgs = compute_rgb_channel_images(original_rgb)

    # --- Channel ablation ---
    logger.info("Computing channel ablation ...")
    try:
        ablation_raw = compute_channel_ablation(
            state.mobilenet_model,
            state.pca,
            state.stacking_clf,
            original_rgb,
            baseline_asd_proba=asd_proba,
            asd_class_idx=asd_class_idx,
        )
        ablation = {k: ChannelAblationResult(**v) for k, v in ablation_raw.items()}
    except Exception as e:
        logger.warning(f"Channel ablation failed: {e}")
        ablation = {}

    # --- Occlusion sensitivity heatmap ---
    logger.info("Computing occlusion sensitivity heatmap ...")
    occlusion_b64 = None
    try:
        occlusion_b64 = compute_occlusion_heatmap(
            state.mobilenet_model,
            state.pca,
            state.stacking_clf,
            original_rgb,
            asd_class_idx=asd_class_idx,
            patch_size=32,
            stride=16,
        )
    except Exception as e:
        logger.warning(f"Occlusion heatmap failed: {e}")

    analysis_id = str(uuid.uuid4())[:8]

    return PredictionResponse(
        success=True,
        prediction=predicted_label,
        confidence=round(confidence, 4),
        asd_probability=round(asd_proba, 4),
        non_asd_probability=round(non_asd_proba, 4),
        model_name="MobileNet + PCA(250) + StackingClassifier",
        model_description=(
            "MobileNet extracts 1024-dim features → PCA reduces to 250 components "
            "(92.1% variance) → StackingClassifier (SVM + KNN → Logistic Regression meta-learner)"
        ),
        explainability=ExplainabilityResult(
            method="Occlusion Sensitivity + Channel Ablation",
            description=(
                "Occlusion Sensitivity: 32×32 gray patches are systematically applied to the image. "
                "Regions where occluding decreases the ASD probability the most are highlighted as important. "
                "Channel Ablation: each RGB channel (Velocity/Acceleration/Jerk) is zeroed out "
                "independently to measure its contribution to the prediction."
            ),
            occlusion_heatmap_b64=occlusion_b64,
            channel_ablation=ablation,
        ),
        visualizations=VisualizationsResult(
            original_b64=channel_imgs["original"],
            red_velocity_b64=channel_imgs["red_velocity"],
            green_acceleration_b64=channel_imgs["green_acceleration"],
            blue_jerk_b64=channel_imgs["blue_jerk"],
        ),
        disclaimer=DISCLAIMER,
        analysis_id=analysis_id,
    )
