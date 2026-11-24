"""
EyeTrace AI — ML Model Loader (Singleton)
Loads MobileNet feature extractor + PCA + Stacking Classifier exactly
as trained in ASD_EyeTracking_Pipeline.ipynb
"""
import os
import logging
import joblib
import numpy as np

logger = logging.getLogger(__name__)

MODELS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "models")
PCA_PATH = os.path.join(MODELS_DIR, "pca_250.pkl")
STACKING_CLF_PATH = os.path.join(MODELS_DIR, "stacking_clf.pkl")

class ModelState:
    """Singleton holding all loaded model artifacts."""
    mobilenet_model = None
    pca = None
    stacking_clf = None
    model_loaded: bool = False
    pca_available: bool = False
    stacking_clf_available: bool = False
    mobilenet_available: bool = False
    load_error: str = ""

    # Class labels as expected from training
    CLASSES = ["Autistic", "Non_Autistic"]

_state = ModelState()


def get_state() -> ModelState:
    return _state


def load_models() -> ModelState:
    """Load all model artifacts. Called once at startup."""
    global _state

    logger.info("=== EyeTrace AI — Loading model artifacts ===")

    # --- Check artifact files ---
    _state.pca_available = os.path.isfile(PCA_PATH)
    _state.stacking_clf_available = os.path.isfile(STACKING_CLF_PATH)

    if not _state.pca_available:
        logger.error(f"[MISSING] pca_250.pkl not found at: {PCA_PATH}")
    else:
        logger.info(f"[OK] pca_250.pkl found ({os.path.getsize(PCA_PATH):,} bytes)")

    if not _state.stacking_clf_available:
        logger.error(f"[MISSING] stacking_clf.pkl not found at: {STACKING_CLF_PATH}")
    else:
        logger.info(f"[OK] stacking_clf.pkl found ({os.path.getsize(STACKING_CLF_PATH):,} bytes)")

    # --- Load sklearn artifacts ---
    if _state.pca_available:
        try:
            _state.pca = joblib.load(PCA_PATH)
            logger.info(f"[OK] PCA loaded: n_components={_state.pca.n_components_}")
        except Exception as e:
            _state.pca_available = False
            _state.load_error = f"PCA load error: {e}"
            logger.error(_state.load_error)

    if _state.stacking_clf_available:
        try:
            _state.stacking_clf = joblib.load(STACKING_CLF_PATH)
            logger.info(f"[OK] StackingClassifier loaded: estimators={[e[0] for e in _state.stacking_clf.estimators]}")
        except Exception as e:
            _state.stacking_clf_available = False
            _state.load_error = f"StackingClassifier load error: {e}"
            logger.error(_state.load_error)

    # --- Load MobileNet feature extractor ---
    try:
        import tensorflow as tf
        from tensorflow.keras.applications import MobileNet
        from tensorflow.keras.models import Model

        logger.info("[...] Loading MobileNet (ImageNet weights, no top, pooling=avg) ...")
        base = MobileNet(
            weights="imagenet",
            include_top=False,
            input_shape=(224, 224, 3),
            pooling="avg",   # GlobalAveragePooling2D → 1024-dim features
        )
        _state.mobilenet_model = base
        _state.mobilenet_available = True
        logger.info(f"[OK] MobileNet loaded: output shape={base.output_shape}")
    except Exception as e:
        _state.mobilenet_available = False
        _state.load_error = f"MobileNet load error: {e}"
        logger.error(_state.load_error)

    # --- Overall readiness ---
    _state.model_loaded = (
        _state.mobilenet_available
        and _state.pca_available
        and _state.stacking_clf_available
    )

    if _state.model_loaded:
        logger.info("=== ✅ All model artifacts loaded — ready for inference ===")
    else:
        logger.warning("=== ⚠️  Some model artifacts missing/failed — inference unavailable ===")

    return _state
