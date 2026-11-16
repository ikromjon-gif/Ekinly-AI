import tempfile
import threading
import unittest
from pathlib import Path
from unittest.mock import patch

import storage


class StorageTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.data_path = Path(self.temp_dir.name) / "history.json"
        self.data_file_patch = patch.object(storage, "DATA_FILE", str(self.data_path))
        self.data_file_patch.start()

    def tearDown(self):
        self.data_file_patch.stop()
        self.temp_dir.cleanup()

    def test_save_and_load_round_trip(self):
        initial = {"predictions": [{"id": 1, "disease_name": "Tomato"}], "next_id": 2}
        storage.save_data(initial)
        self.assertEqual(storage.load_data(), initial)

    def test_save_prediction_assigns_sequential_ids(self):
        first = storage.save_disease_prediction("Tomato___healthy", 99.2, "Tomato")
        second = storage.save_disease_prediction("Potato___Early_blight", 97.1, "Potato")
        self.assertEqual((first, second), (1, 2))
        self.assertEqual(storage.load_data()["next_id"], 3)

    def test_concurrent_saves_keep_all_records_and_unique_ids(self):
        total = 24
        ids = []
        errors = []

        def save_one(index):
            try:
                ids.append(
                    storage.save_disease_prediction(
                        f"disease-{index}", 90.0, "plant"
                    )
                )
            except Exception as exc:  # surfaced to the test thread's main context
                errors.append(exc)

        threads = [threading.Thread(target=save_one, args=(i,)) for i in range(total)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

        self.assertEqual(errors, [])
        self.assertEqual(sorted(ids), list(range(1, total + 1)))
        self.assertEqual(len(storage.load_data()["predictions"]), total)


if __name__ == "__main__":
    unittest.main()
