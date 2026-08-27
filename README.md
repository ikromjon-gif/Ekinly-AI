# 🌿 AI Plant Disease Detection

A deep learning–based plant disease classification system developed as part of a Master's thesis at Chonnam National University.

The project combines **MobileNetV2** and **EfficientNetB0** through feature-level fusion and selective fine-tuning to classify plant leaf images into **38 disease/healthy classes**.

## 🚀 Live Demo

**Hugging Face Space:**
https://huggingface.co/spaces/IKROMJON01/plant-disease-detection-demo

The deployed Gradio application supports image upload, top-3 predictions, confidence scores, multilingual interaction (English / Korean / Uzbek), prediction history, statistics, and optional AI-assisted recommendations.

## 🧠 Model Architecture

```text
                 Plant Leaf Image
                        │
                 Preprocessing
                        │
          ┌─────────────┴─────────────┐
          │                           │
     MobileNetV2                 EfficientNetB0
   lightweight features          semantic features
          │                           │
          └───────────┬───────────────┘
                      │
               Feature Fusion
                      │
                Dense + Dropout
                      │
                  Softmax (38)
                      │
              Disease Prediction
```

### Key configuration

| Component | Configuration |
|---|---|
| Dataset | PlantVillage |
| Images | 54,704 |
| Classes | 38 |
| Input | 224 × 224 × 3 |
| Backbones | MobileNetV2 + EfficientNetB0 |
| Fusion | Feature-level concatenation |
| Transfer learning | ImageNet pretrained weights |
| Fine-tuning | Selective upper-layer fine-tuning |
| Optimizer | Adam |
| Loss | Categorical Cross-Entropy |
| Batch size | 64 |

## 📊 Results

The final fine-tuned hybrid model achieved **98.90% validation accuracy** on the PlantVillage evaluation setup used in the thesis.

The evaluation included Accuracy, Precision, Recall, F1-score, and confusion-matrix analysis.

> **Important:** The 98.90% result is a validation result on the controlled PlantVillage dataset. Performance on real-world field images may be lower because of changes in lighting, background, image quality, and environmental conditions.

## ✨ Application Features

- 🌱 Plant disease classification from leaf images
- 🔬 Top-3 disease predictions with confidence scores
- 🌍 English, Korean, and Uzbek interface
- 🤖 Optional Gemini-based AI recommendations
- 📊 Prediction history and statistics
- 📍 Browser geolocation prototype
- ⚡ Gradio-based web deployment
- ☁️ Hosted on Hugging Face Spaces

## 🛠️ Technology Stack

- Python
- TensorFlow / Keras
- MobileNetV2
- EfficientNetB0
- NumPy
- Pillow
- OpenCV
- Gradio
- Google Generative AI API
- Hugging Face Spaces
- Google Colab

## 📁 Repository Structure

```text
plant_disease_detection/
├── app.py                 # Original Flask prototype / reference implementation
├── leaf pictures/         # Example leaf images
├── static/
│   └── logo.png
├── requirements.txt
├── .gitignore
└── README.md
```

> The current production/demo implementation is deployed and maintained in the linked Hugging Face Space. The GitHub repository is being organized as the project source/documentation repository.

## 🔬 Research Context

This project is based on the Master's thesis:

**Hybrid Deep Learning Framework for Plant Disease Classification Using MobileNetV2 and EfficientNetB0 Feature Fusion**

Department of Computer Engineering, Graduate School, Chonnam National University, 2026.

## ⚠️ Limitations

The model was evaluated primarily on PlantVillage, whose images are collected under controlled conditions. It should therefore be treated as a research/educational prototype rather than a substitute for professional agricultural diagnosis.

Future work includes evaluation on field-collected datasets, improved domain generalization, attention mechanisms, Vision Transformers, model compression, and edge/mobile deployment.

## 👨‍💻 Author

**Ikromjon Tojiboev**  
Computer Engineering — Chonnam National University

---

⭐ If you find the project useful, feel free to explore the live demo and research documentation.