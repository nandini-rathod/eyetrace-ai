"""Health check endpoint."""
from fastapi import APIRouter
from app.ml.model import get_state
from app.schemas.prediction import HealthResponse, ArtifactStatus

router = APIRouter()


@router.get("/api/health", response_model=HealthResponse)
async def health_check():
    state = get_state()
    return HealthResponse(
        status="ok",
        model_loaded=state.model_loaded,
        artifacts=ArtifactStatus(
            pca_250=state.pca_available,
            stacking_clf=state.stacking_clf_available,
            mobilenet=state.mobilenet_available,
        ),
        model_name="MobileNet + PCA(250) + StackingClassifier",
        model_description=(
            "MobileNet (ImageNet pretrained, no top, GlobalAveragePooling) → "
            "1024-dim features → PCA (250 components, 92.1% variance) → "
            "StackingClassifier (SVM + KNN base, Logistic Regression meta)"
        ),
        load_error=state.load_error or None,
    )
