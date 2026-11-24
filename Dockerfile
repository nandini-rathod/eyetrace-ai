# ==========================================
# Multi-Stage Dockerfile for EyeTrace AI
# Serves both React Frontend and FastAPI ML Backend
# Compatible with: Hugging Face Spaces, Render, Cloud Run, Railway, Fly.io
# ==========================================

# --- Stage 1: Build React Frontend ---
FROM node:18-alpine AS frontend-builder
WORKDIR /app/frontend

COPY frontend/package*.json ./
RUN npm install

COPY frontend/ ./
RUN npm run build

# --- Stage 2: Python ML Backend & Server ---
FROM python:3.10-slim

# Prevent Python from writing .pyc and enable unbuffered logging
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=7860

WORKDIR /app

# Install system dependencies for OpenCV and Pillow
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python requirements
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt httpx

# Pre-download and cache MobileNet weights inside the image
RUN python -c "from tensorflow.keras.applications import MobileNet; MobileNet(weights='imagenet', include_top=False, input_shape=(224, 224, 3), pooling='avg')"

# Copy backend application and model files
COPY backend/app ./backend/app
COPY backend/models ./backend/models
COPY backend/static ./backend/static

# Copy built frontend assets from Stage 1
COPY --from=frontend-builder /app/frontend/dist ./frontend/dist

# Expose port (7860 is default for Hugging Face Spaces, dynamically overridden by $PORT on Render/Cloud Run)
EXPOSE 7860

WORKDIR /app/backend

# Start uvicorn server binding to 0.0.0.0 and $PORT
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-7860}"]
