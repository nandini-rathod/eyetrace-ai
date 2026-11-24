"""
EyeTrace AI — FastAPI Application Entry Point
"""
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.ml.model import load_models
from app.routes import health, predict

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Load model artifacts at startup."""
    logger.info("EyeTrace AI backend starting up ...")
    load_models()
    yield
    logger.info("EyeTrace AI backend shutting down.")


app = FastAPI(
    title="EyeTrace AI",
    description=(
        "Research API for ASD eye-tracking scanpath classification. "
        "Uses MobileNet + PCA + StackingClassifier pipeline. "
        "For academic/research purposes only — NOT a clinical diagnostic tool."
    ),
    version="1.0.0",
    lifespan=lifespan,
)

# CORS — allow React dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files (comparison PNGs etc.)
import os
static_dir = os.path.join(os.path.dirname(__file__), "..", "static")
os.makedirs(static_dir, exist_ok=True)
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Routers
app.include_router(health.router)
app.include_router(predict.router)

# Mount frontend build if available (production single-container mode)
dist_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "frontend", "dist"))
if not os.path.exists(dist_dir):
    # Fallback if inside container where frontend dist is copied into /app/frontend/dist or /app/dist
    dist_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "dist"))

if os.path.exists(dist_dir):
    logger.info(f"Serving frontend static build from: {dist_dir}")
    # Mount assets subfolder
    assets_dir = os.path.join(dist_dir, "assets")
    if os.path.exists(assets_dir):
        app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")

    from fastapi.responses import FileResponse

    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        file_path = os.path.join(dist_dir, full_path)
        if os.path.isfile(file_path):
            return FileResponse(file_path)
        return FileResponse(os.path.join(dist_dir, "index.html"))
else:
    @app.get("/")
    async def root():
        return {
            "app": "EyeTrace AI Backend",
            "version": "1.0.0",
            "docs": "/docs",
            "health": "/api/health",
            "predict": "/api/v1/predict  [POST]",
        }
