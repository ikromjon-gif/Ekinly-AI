"""Inference utilities for Ekinly AI's plant disease classifier."""
import numpy as np
from PIL import Image, ImageEnhance


def preprocess_image(image):
    """Apply the app's image enhancement, resize, and EfficientNet preprocessing."""
    if not isinstance(image, Image.Image):
        raise TypeError("image must be a PIL.Image.Image")
    enhanced = ImageEnhance.Contrast(image).enhance(1.2)
    enhanced = ImageEnhance.Sharpness(enhanced).enhance(1.3)
    resized = enhanced.resize((224, 224))
    array = np.asarray(resized)
    # tf.keras EfficientNet preprocess_input is a pass-through (rescaling is in-model).
    return np.expand_dims(array, axis=0)


def predict_top_k(model, image, class_names, k=3):
    """Return top-k class names and confidence percentages from model predictions."""
    if model is None:
        raise ValueError("model must not be None")
    if not class_names:
        raise ValueError("class_names must not be empty")
    if k < 1:
        raise ValueError("k must be at least 1")

    scores = np.asarray(model.predict(preprocess_image(image), verbose=0))[0]
    if scores.ndim != 1 or len(scores) != len(class_names):
        raise ValueError("model output size must match class_names")

    top_indices = np.argsort(scores)[-min(k, len(class_names)):][::-1]
    return [(class_names[int(i)], float(scores[i]) * 100.0) for i in top_indices]
