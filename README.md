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