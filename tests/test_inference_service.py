import unittest

import numpy as np
from PIL import Image

from inference_service import predict_top_k, preprocess_image


class FakeModel:
    def __init__(self, scores):
        self.scores = np.asarray(scores, dtype=np.float32)
        self.input_shape = None

    def predict(self, inputs, verbose=0):
        self.input_shape = inputs.shape
        return self.scores[np.newaxis, :]


class InferenceServiceTests(unittest.TestCase):
    def setUp(self):
        self.image = Image.new("RGB", (80, 60), color=(100, 150, 200))

    def test_preprocessing_returns_batch_of_224_rgb_images(self):
        processed = preprocess_image(self.image)
        self.assertEqual(processed.shape, (1, 224, 224, 3))
        self.assertTrue(np.isfinite(processed).all())

    def test_predict_top_k_returns_sorted_class_confidences(self):
        model = FakeModel([0.15, 0.70, 0.10, 0.05])
        results = predict_top_k(model, self.image, ["a", "b", "c", "d"], k=3)
        self.assertEqual([name for name, _ in results], ["b", "a", "c"])
        self.assertAlmostEqual(results[0][1], 70.0, places=5)
        self.assertEqual(model.input_shape, (1, 224, 224, 3))

    def test_rejects_output_size_mismatch(self):
        model = FakeModel([0.2, 0.8])
        with self.assertRaisesRegex(ValueError, "output size"):
            predict_top_k(model, self.image, ["only-one-class"])

    def test_rejects_invalid_k(self):
        model = FakeModel([1.0])
        with self.assertRaisesRegex(ValueError, "at least 1"):
            predict_top_k(model, self.image, ["class"], k=0)


if __name__ == "__main__":
    unittest.main()
