# 🌱 Ekinly AI

> **AI-powered plant disease detection for smarter agriculture.**

Ekinly AI is a deep learning–based plant disease classification application developed as part of a Master's research project at **Chonnam National University**.

The system uses a hybrid **MobileNetV2 + EfficientNetB0** model with feature-level fusion to classify plant leaf images into **38 classes**. The current application is deployed as an interactive **Gradio** web app on Hugging Face Spaces and supports English, Korean, and Uzbek.

## 🚀 Live Demo

**[Try Ekinly AI on Hugging Face](https://huggingface.co/spaces/IKROMJON01/Ekinly-Ai)**

The live application currently provides:

- 🌿 Leaf image upload and disease prediction
- 🔬 Top-3 predictions with confidence scores
- 🌍 English / Korean / Uzbek interface
- 🤖 Optional Gemini-powered agricultural advice
- 📊 Prediction history and basic statistics
- 📍 Browser-based location sharing prototype
- ⚡ Gradio web interface

## 🧠 Model Architecture

```text
                    Plant Leaf Image
                           │
                    Image Preprocessing
                           │
             ┌─────────────┴─────────────┐
             │                           │
        MobileNetV2                EfficientNetB0
      Lightweight Features        Semantic Features
             │                           │
             └─────────────┬─────────────┘
                           │
                    Feature Fusion
                           │
                      Dense Layer
                           │
                        Dropout
                           │
                     Softmax (38)
                           │
                  Disease Prediction
```

### Model configuration

| Component | Configuration |
|---|---|
| Dataset | PlantVillage |
| Classes | 38 |
| Input size | 224 × 224 × 3 |
| Backbone 1 | MobileNetV2 |
| Backbone 2 | EfficientNetB0 |
| Fusion | Feature-level concatenation |
| Transfer learning | ImageNet pretrained weights |
| Fine-tuning | Selective upper-layer fine-tuning |
| Optimizer | Adam |
| Loss | Categorical Cross-Entropy |
| Batch size | 64 |

## 📊 Performance

The final fine-tuned hybrid model achieved **98.90% validation accuracy** on the PlantVillage evaluation setup used in the research.

The research evaluation also considered **precision, recall, F1-score, and confusion-matrix analysis**.

> **Note:** 98.90% is a validation result on the PlantVillage dataset. Performance on field images can differ because of lighting, background, image quality, plant variety, and other real-world conditions.

## 🌱 Supported Plants

The current model covers the following plant categories:

**Apple · Blueberry · Cherry · Corn · Grape · Orange · Peach · Pepper Bell · Potato · Raspberry · Soybean · Squash · Strawberry · Tomato**

Across these categories, the model predicts **38 disease/healthy classes**.

## ✨ Application Features

### 🔍 Disease Detection

Upload a plant leaf image and Ekinly AI returns the three highest-probability predictions with confidence scores and disease descriptions.

### 🤖 AI Agricultural Advice

When the Gemini API is configured through the `GEMINI_API_KEY` environment variable, the application can generate short AI-assisted advice related to the predicted condition.

### 🌍 Multilingual Interface

The interface supports:

- 🇬🇧 English
- 🇰🇷 Korean
- 🇺🇿 Uzbek

### 📊 History & Statistics

Predictions can be stored in `diseases_data.json` and used to display recent prediction history and basic disease/plant statistics.

### 📍 Location Prototype

The application includes browser geolocation functionality for sharing the user's current location. The current implementation displays the location in the interface; it is a prototype for future disease-mapping functionality.

## 🛠️ Technology Stack

- **Python**
- **TensorFlow / Keras**
- **MobileNetV2**
- **EfficientNetB0**
- **NumPy**
- **Pillow**
- **OpenCV**
- **Gradio**
- **Google Generative AI / Gemini**
- **Hugging Face Spaces**
- **Google Colab**

## 📁 Project Structure

```text
Ekinly-AI/
├── app.py
├── proposed_hybrid_finetuned_final.keras
├── diseases_data.json
├── logo.png
├── requirements.txt
├── LICENSE
├── .gitignore
└── README.md
```

> The exact files in the repository may evolve as the project is developed. The deployed application uses the same core model and application code documented here.

## 🔬 Research Context

Ekinly AI is based on the Master's research project:

**Hybrid Deep Learning Framework for Plant Disease Classification Using MobileNetV2 and EfficientNetB0 Feature Fusion**

**Department of Computer Engineering**  
**Graduate School, Chonnam National University**  
**2026**

The project explores how complementary lightweight and efficient CNN architectures can be combined through feature fusion for plant disease classification.

## ⚠️ Limitations

- The model is primarily evaluated on the controlled **PlantVillage** dataset.
- Real-world field conditions may produce lower performance.
- Gemini advice is AI-generated and should not be treated as professional agricultural diagnosis.
- The current GPS functionality is a prototype and does not yet provide a complete disease-spread mapping system.
- The current application is a research/portfolio prototype rather than a production agricultural diagnostic service.

## 🔮 Future Direction

Ekinly AI is designed with a broader smart-agriculture vision in mind. Potential future development includes:

- 🌾 Field-image disease detection
- 🛰️ Satellite and drone-based crop monitoring
- 📈 Crop health and yield prediction
- 🗺️ Disease distribution mapping
- 🤖 Agricultural AI assistant
- 📚 Retrieval-Augmented Generation (RAG) for agricultural knowledge
- 📱 Edge/mobile model optimization
- 🌱 Broader crop and disease coverage

## 👨‍💻 Author

**Ikromjon Tojiboev**  
M.S. Computer Engineering, Chonnam National University

---

⭐ **Ekinly AI** is an evolving AI-agriculture project combining deep learning, computer vision, and practical web deployment.