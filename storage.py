"""JSON-backed prediction history storage for Ekinly AI.

Writes are atomic and read-modify-write operations are protected by a process-local
lock. For multi-process deployments, use a database with transactional locking.
"""
import json
import os
import tempfile
import threading
from datetime import datetime

DATA_FILE = "diseases_data.json"
_DATA_LOCK = threading.RLock()


def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    return {"predictions": [], "next_id": 1}


def save_data(data):
    """Persist JSON atomically so readers never observe a partial file."""
    directory = os.path.dirname(os.path.abspath(DATA_FILE))
    fd, temp_path = tempfile.mkstemp(
        prefix=".diseases_data-", suffix=".tmp", dir=directory
    )
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=2, ensure_ascii=False)
            file.flush()
            os.fsync(file.fileno())
        os.replace(temp_path, DATA_FILE)
    except Exception:
        try:
            os.unlink(temp_path)
        except OSError:
            pass
        raise


def save_disease_prediction(
    disease_name, confidence, plant_type, latitude=None, longitude=None
):
    """Append a prediction with a sequential ID under the local process lock."""
    with _DATA_LOCK:
        data = load_data()
        prediction = {
            "id": data["next_id"],
            "disease_name": disease_name,
            "confidence": confidence,
            "latitude": latitude,
            "longitude": longitude,
            "plant_type": plant_type,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        data["predictions"].append(prediction)
        data["next_id"] += 1
        save_data(data)
        print(f"Prediction saved. ID: {prediction['id']}")
        return prediction["id"]


def get_disease_history(limit=50):
    data = load_data()
    predictions = sorted(
        data["predictions"], key=lambda item: item["timestamp"], reverse=True
    )
    return predictions[:limit]


def get_statistics():
    predictions = load_data()["predictions"]
    if not predictions:
        return {"total": 0, "by_disease": {}, "by_plant": {}}
    by_disease = {}
    by_plant = {}
    for prediction in predictions:
        disease = prediction["disease_name"]
        plant = prediction["plant_type"]
        by_disease[disease] = by_disease.get(disease, 0) + 1
        by_plant[plant] = by_plant.get(plant, 0) + 1
    return {
        "total": len(predictions),
        "by_disease": by_disease,
        "by_plant": by_plant,
    }


def get_disease_locations():
    locations = []
    for prediction in load_data()["predictions"]:
        if prediction.get("latitude") and prediction.get("longitude"):
            locations.append(
                {
                    "latitude": prediction["latitude"],
                    "longitude": prediction["longitude"],
                    "disease_name": prediction["disease_name"],
                    "confidence": prediction["confidence"],
                    "plant_type": prediction["plant_type"],
                    "timestamp": prediction["timestamp"],
                }
            )
    return locations
