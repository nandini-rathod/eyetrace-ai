---
title: EyeTrace AI
emoji: 👁️
colorFrom: blue
colorTo: indigo
sdk: docker
app_port: 7860
pinned: false
license: mit
---

# EyeTrace AI

**Explainable ASD Eye-Tracking Scanpath Classification**

> ⚠️ **Academic research project only. Not a clinical diagnostic tool.**

---

## Deploying to Hugging Face Spaces (Free 16GB RAM Tier)

EyeTrace AI is pre-configured for instant 1-click Docker deployment to **Hugging Face Spaces**:

1. Go to [Hugging Face Spaces](https://huggingface.co/new-space).
2. Choose a name (e.g. `eyetrace-ai`), select license (e.g. `mit`), and choose **Space SDK: Docker** (Blank).
3. Under Hardware, select the default **Free CPU (2 vCPU, 16 GB RAM)**.
4. In your terminal at `c:\Users\pranav\Desktop\ASD`, link and push:
   ```bash
   git remote add space https://huggingface.co/spaces/<YOUR-USERNAME>/<YOUR-SPACE-NAME>
   git push space master:main
   ```
5. Hugging Face will automatically build the multi-stage Docker container (compiling the React frontend and launching the FastAPI inference backend) and publish your live web application!

---

## Overview

EyeTrace AI is a full-stack web application that classifies eye-tracking scanpath images as **ASD** or **Non-ASD** using a locally trained machine learning model. All inference runs on your machine — no external AI APIs are used.

**Pipeline:**
```
Scanpath Image → Preprocessing → MobileNet (1024-dim) → PCA (250 components) → StackingClassifier → ASD / Non-ASD
```

**Explainability:**
- Occlusion Sensitivity (32×32 patch-based heatmap)
- Channel Ablation (Velocity / Acceleration / Jerk channel contributions)

---

## Technology Stack

| Layer | Stack |
|---|---|
| Frontend | React + Vite + Tailwind CSS + React Router + Axios + Lucide + Recharts |
| Backend | Python + FastAPI + Uvicorn |
| ML | TensorFlow/Keras (MobileNet) + scikit-learn (PCA, StackingClassifier) |
| Image | Pillow + OpenCV (headless) |

---

## Project Structure

```
ASD/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI app entry point
│   │   ├── routes/
│   │   │   ├── health.py        # GET /api/health
│   │   │   └── predict.py       # POST /api/v1/predict
│   │   ├── ml/
│   │   │   ├── model.py         # Model loader singleton
│   │   │   └── inference.py     # Preprocessing + inference pipeline
│   │   ├── schemas/
│   │   │   └── prediction.py    # Pydantic response models
│   │   └── utils/
│   │       └── explainability.py # Occlusion sensitivity + channel ablation
│   ├── models/
│   │   ├── pca_250.pkl          # Trained PCA (250 components)
│   │   └── stacking_clf.pkl     # Trained StackingClassifier
│   ├── requirements.txt
│   └── venv/                    # Python virtual environment (not committed)
├── frontend/
│   ├── src/
│   │   ├── components/          # Navbar, Footer, ImageUploader, etc.
│   │   ├── pages/               # LandingPage, AnalysisPage, ResultsPage, ResearchPage
│   │   ├── services/api.js      # Axios client
│   │   └── App.jsx              # React Router setup
│   ├── .env.local               # VITE_API_URL=http://127.0.0.1:8000
│   └── package.json
├── start_backend.bat
├── start_frontend.bat
└── README.md
```

---

## Setup Instructions (Windows)

### Prerequisites
- Python 3.10+ (with `python` on PATH)
- Node.js 18+ (with `npm` on PATH)

### 1. Model Artifacts

The model artifacts must be in `backend/models/`:

```
backend/models/pca_250.pkl          (from ASD_Model_Outputs/)
backend/models/stacking_clf.pkl     (from ASD_Model_Outputs/)
```

They are already copied here from `ASD_Model_Outputs/` during setup.

### 2. Backend Setup

```powershell
cd c:\Users\pranav\Desktop\ASD\backend

# Create virtual environment
python -m venv venv

# Activate it
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
pip install tensorflow   # ~600 MB — may take a few minutes
```

### 3. Frontend Setup

```powershell
cd c:\Users\pranav\Desktop\ASD\frontend
npm install
```

---

## Running the Application

### Option A: Use the batch files (easiest)

Open **two separate Command Prompt windows**:

**Window 1 — Backend:**
```
double-click: start_backend.bat
```

**Window 2 — Frontend:**
```
double-click: start_frontend.bat
```

### Option B: Manual

**Terminal 1 — Backend:**
```powershell
cd c:\Users\pranav\Desktop\ASD\backend
.\venv\Scripts\Activate.ps1
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

**Terminal 2 — Frontend:**
```powershell
cd c:\Users\pranav\Desktop\ASD\frontend
npm run dev
```

Then open: **http://localhost:5173**

---

## API Endpoints

### `GET /api/health`
Check backend and model status.

```json
{
  "status": "ok",
  "model_loaded": true,
  "artifacts": {
    "pca_250": true,
    "stacking_clf": true,
    "mobilenet": true
  },
  "model_name": "MobileNet + PCA(250) + StackingClassifier",
  "model_description": "..."
}
```

### `POST /api/v1/predict`
Submit a scanpath image for classification.

- **Request:** `multipart/form-data`, field `image` (PNG/JPG/JPEG, max 10 MB)
- **Response:**
```json
{
  "success": true,
  "prediction": "ASD",
  "confidence": 0.812,
  "asd_probability": 0.812,
  "non_asd_probability": 0.188,
  "model_name": "MobileNet + PCA(250) + StackingClassifier",
  "explainability": {
    "method": "Occlusion Sensitivity + Channel Ablation",
    "occlusion_heatmap_b64": "...",
    "channel_ablation": { ... }
  },
  "visualizations": {
    "original_b64": "...",
    "red_velocity_b64": "...",
    "green_acceleration_b64": "...",
    "blue_jerk_b64": "..."
  },
  "disclaimer": "...",
  "analysis_id": "a3f2b9c1"
}
```

Interactive API docs: **http://127.0.0.1:8000/docs**

---

## ML Pipeline Details

| Step | Detail |
|---|---|
| Input | RGB image, any size |
| Resize | 224 × 224 (LANCZOS) |
| Blur | Gaussian blur, kernel 5×5, σ=0 |
| Normalization | `mobilenet.preprocess_input` (scales to [-1, 1]) |
| Feature extractor | MobileNet, ImageNet weights, `include_top=False`, `pooling='avg'` → **1024-dim** |
| PCA | 250 components, 92.1% explained variance, loaded from `pca_250.pkl` |
| Classifier | StackingClassifier (SVM + KNN base, Logistic Regression meta), loaded from `stacking_clf.pkl` |

---

## Explainability Methods

### Occlusion Sensitivity
A 32×32 gray (128,128,128) patch is slid over the image with stride 16. The full pipeline is re-run for each patch position. The heatmap shows regions whose occlusion causes the largest drop in ASD probability. These are the image regions most influential to the classification.

This is a **model attribution map** — not a clinical gaze heatmap or behavioral indicator.

### Channel Ablation
Each RGB channel (Red=Velocity, Green=Acceleration, Blue=Jerk) is independently zeroed out. The delta in ASD probability measures each kinematic feature's contribution.

> **Note:** Grad-CAM is NOT used. The sklearn StackingClassifier breaks the gradient graph. Occlusion sensitivity is model-agnostic and mathematically valid for this pipeline.

---

## Dataset (from notebook)

| Property | Value |
|---|---|
| ASD samples | 219 |
| Non-ASD samples | 328 |
| Total | 547 |
| PCA components | 250 |
| Explained variance | 92.1% |
| Framework | TensorFlow 2.x + scikit-learn |
| Random seed | 42 |

---

## Disclaimer

This tool is for **academic and research purposes only**. It must not be used as a clinical diagnostic instrument. The model has not been clinically validated and was trained on a small, limited dataset. ASD diagnosis requires comprehensive multidisciplinary clinical evaluation by qualified healthcare professionals.

---

## Troubleshooting

| Issue | Fix |
|---|---|
| `uvicorn: command not found` | Activate venv: `.\venv\Scripts\Activate.ps1` |
| `No module named tensorflow` | `pip install tensorflow` inside venv |
| Backend shows model_loaded: false | Check `backend/models/` contains both `.pkl` files |
| Frontend shows "Backend offline" | Ensure backend is running on port 8000 |
| Occlusion heatmap is slow | Normal — it runs ~100+ forward passes. CPU will take 60–120s |
| PowerShell `&&` error | Use `;` instead, or run commands separately |
