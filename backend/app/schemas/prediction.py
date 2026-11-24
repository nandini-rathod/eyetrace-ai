"""Pydantic schemas for EyeTrace AI API responses."""
from pydantic import BaseModel
from typing import Optional, Dict, Any, List


class ArtifactStatus(BaseModel):
    pca_250: bool
    stacking_clf: bool
    mobilenet: bool


class HealthResponse(BaseModel):
    status: str
    model_loaded: bool
    artifacts: ArtifactStatus
    model_name: str
    model_description: str
    load_error: Optional[str] = None


class ChannelAblationResult(BaseModel):
    baseline_asd_probability: float
    ablated_asd_probability: float
    delta: float
    importance: float
    direction: str


class ExplainabilityResult(BaseModel):
    method: str
    description: str
    occlusion_heatmap_b64: Optional[str] = None
    channel_ablation: Optional[Dict[str, ChannelAblationResult]] = None


class VisualizationsResult(BaseModel):
    original_b64: str
    red_velocity_b64: str
    green_acceleration_b64: str
    blue_jerk_b64: str


class PredictionResponse(BaseModel):
    success: bool
    prediction: str              # "ASD" or "Non-ASD"
    confidence: float            # max probability
    asd_probability: float
    non_asd_probability: float
    model_name: str
    model_description: str
    explainability: ExplainabilityResult
    visualizations: VisualizationsResult
    disclaimer: str
    analysis_id: str


class ErrorResponse(BaseModel):
    success: bool = False
    error: str
    detail: Optional[str] = None
