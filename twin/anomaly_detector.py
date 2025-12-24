import os
import joblib
import numpy as np
from sklearn.ensemble import IsolationForest

MODEL_DIR = os.path.join(os.path.dirname(__file__), "..", "models")
os.makedirs(MODEL_DIR, exist_ok=True)

class AnomalyDetector:
    def __init__(self):
        self.model = IsolationForest(contamination=0.05, random_state=42)
        self.is_fitted = False

    def fit(self, X):
        self.model.fit(X)
        self.is_fitted = True

    def is_anomaly(self, X):
        if not self.is_fitted or len(X) == 0:
            return [False] * len(X)
        preds = self.model.predict(X)
        return (preds == -1).tolist()

    def save(self, name="anomaly_iforest.pkl"):
        joblib.dump(self.model, os.path.join(MODEL_DIR, name))

    def load(self, name="anomaly_iforest.pkl"):
        path = os.path.join(MODEL_DIR, name)
        if os.path.exists(path):
            self.model = joblib.load(path)
            self.is_fitted = True
