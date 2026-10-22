# 🌱 Ekinly AI

> **Hybrid deep learning for plant disease classification and smart-agriculture applications.**

Ekinly AI is a Master's research project at **Chonnam National University** that investigates feature-level fusion of **MobileNetV2 and EfficientNetB0** for plant disease classification.

**Live demo:** https://huggingface.co/spaces/IKROMJON01/Ekinly-Ai

## Problem

Plant disease classification involves a trade-off between lightweight inference and expressive visual representations. Ekinly explores whether complementary CNN backbones can improve classification through feature-level fusion.

## Method

```
Plant Leaf Image
       |
       v
Preprocessing (224 x 224)
       |
 +-----+---------+
 |               |
 v               v
MobileNetV2   EfficientNetB0
 |               |
 +-------+-------+
         |
         v
   Feature Fusion
         |
         v
   Dense + Dropout
         |
         v
   Softmax (38)
```

| Component | Configuration |
|---|---|
| Dataset | PlantVillage |
| Classes | 38 |
| Input | 224 x 224 x 3 |
| Backbones | MobileNetV2 + EfficientNetB0 |
| Initialization | ImageNet pretrained weights |
| Fusion | Feature-level concatenation |
| Fine-tuning | Selective upper-layer fine-tuning |
| Optimizer | Adam |
| Loss | Categorical Cross-Entropy |
| Batch size | 64 |

## Result

**98.90% validation accuracy** on the documented PlantVillage evaluation setup.

The research evaluation also considers precision, recall, F1-score, and confusion-matrix analysis.

> This is a validation result on a controlled dataset, not a claim of equivalent field performance.

## Application

- Leaf image classification
- Top-3 predictions with confidence scores
- English / Korean / Uzbek UI
- Optional Gemini-powered agricultural guidance
- Prediction history and statistics
- Prototype browser geolocation

## Stack

Python · TensorFlow/Keras · MobileNetV2 · EfficientNetB0 · OpenCV · Gradio · Gemini API · Hugging Face Spaces

## Research Context

**Hybrid Deep Learning Framework for Plant Disease Classification Using MobileNetV2 and EfficientNetB0 Feature Fusion**

**M.S. Computer Engineering — Chonnam National University, 2026**

## Limitations

- PlantVillage is controlled; field conditions can differ substantially.
- Validation accuracy does not establish real-world diagnostic reliability.
- Gemini output is AI-generated guidance.
- The project is a research/portfolio prototype, not a certified diagnostic service.

## Future Work

- Field-image evaluation and cross-dataset testing
- Fusion ablation studies
- Calibration and uncertainty estimation
- Edge/mobile optimization
- RAG-based agricultural assistant
- Disease distribution mapping

**Author:** Ikromjon Tojiboev

## Run locally or with Docker

### Python

Use Python 3.10 and install the dependencies:

```bash
python -m venv .venv
# Linux/macOS
source .venv/bin/activate
# Windows PowerShell: .venv\\Scripts\\Activate.ps1
pip install -r requirements.txt
python app.py
```

The app expects the trained model file `proposed_hybrid_finetuned_final.keras` in the project directory by default. Configure `MODEL_PATH` if it is mounted elsewhere. Alternatively, set `MODEL_URL` to a direct HTTPS URL for the model; the app downloads it at startup if the configured file does not already exist. Keep private or access-token-protected URLs out of source control and use deployment secrets.

Optional Gemini guidance requires `GEMINI_API_KEY`. The app can be started without it, but Gemini-based advice will be unavailable.

### Docker

```bash
docker build -t ekinly-ai .
docker run --rm -p 7860:7860 \
  -e MODEL_PATH=/models/proposed_hybrid_finetuned_final.keras \
  -v /absolute/path/to/model-directory:/models:ro \
  ekinly-ai
```

If using a direct model URL instead of a mounted model, pass `-e MODEL_URL=https://your-hosted-direct-model-url`. Replace the example URL and local mount path with your actual values. Configure `GEMINI_API_KEY` through your deployment platform's secret manager if needed.

### Deployment notes

- The trained `.keras` model is not stored in this GitHub repository. A deployment must mount it or provide a direct HTTPS `MODEL_URL`.
- The model may be large; confirm your host's memory, disk, build-time and request-time limits before deploying.
- Prediction history is currently stored in a local `diseases_data.json` file. Container restarts or multiple replicas may lose or split that data; use persistent storage or a database for production.
- The included GitHub Actions workflow checks Python syntax, dependency declarations, and Docker image buildability. It is not a full inference or security test.
- Do not commit API keys or model access tokens.

## MLOps and deployment readiness

### Current automated checks

The GitHub Actions workflow runs on pushes to `main` and `audit/**`, and on pull requests targeting `main`. It currently checks:

- Python syntax compilation for `app.py`
- Presence of key direct dependencies in `requirements.txt`
- Docker image build

Workflow results: https://github.com/ikromjon-gif/Ekinly-AI/actions

These checks confirm source-level consistency and image buildability; they do **not** prove that the hosted model downloads successfully, that TensorFlow can load the model in every deployment environment, or that inference quality is correct. Perform a real inference smoke test after deployment.

### Deployment smoke-test checklist

1. Confirm the service starts and the Gradio page loads.
2. Check logs for `Model loaded from:` and ensure no `Model download failed` or `Model load error` messages appear.
3. Upload a known leaf image and confirm that three predictions are returned.
4. Confirm that the prediction history behaves as expected after a restart.
5. Never place API keys or private model tokens in Git.

### Operational limitations

- The model is hosted separately from this repository. The default `MODEL_URL` points to the public Hugging Face Space file; set `MODEL_PATH` for a mounted model or override `MODEL_URL` when deploying elsewhere.
- Startup requires network access if the model file is not already present.
- Model download and TensorFlow initialization can increase cold-start time and memory usage.
- Prediction history uses a local JSON file, which is not suitable for durable multi-replica production storage.
- Gemini advice is optional and depends on `GEMINI_API_KEY`; core classification should be validated independently.
- The reported 98.90% validation accuracy is from the documented PlantVillage evaluation setup, not a guarantee of field performance.

### Suggested next production improvements

- Add a dedicated automated inference test with a versioned sample image and expected output shape.
- Add model checksum/version tracking and artifact provenance.
- Move prediction history to persistent storage if durable history is required.
- Add structured logs and service-level monitoring.
- Evaluate on field images and measure calibration before presenting the model as a reliable diagnostic system.
