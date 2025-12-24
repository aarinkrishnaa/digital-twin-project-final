import os
import numpy as np
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

MODEL_DIR = os.path.join(os.path.dirname(__file__), "..", "models")
os.makedirs(MODEL_DIR, exist_ok=True)

class PredictiveMaintenance:
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=50, random_state=42)
        self.is_fitted = False
        self.model_path = os.path.join(MODEL_DIR, "pm_rf.pkl")

    def _prepare_features(self, df):
        return df[["temperature", "vibration", "rpm", "current", "load"]].fillna(0).values

    def _generate_labels(self, df):
        cond = (
            (df["vibration"] > 6.0) |
            (df["temperature"] > 75) |
            (df["rpm"] > 1700) |
            (df["current"] > 11)
        )
        return cond.astype(int).values

    def train(self, df):
        if len(df) < 30:
            return False

        X = self._prepare_features(df)
        y = self._generate_labels(df)

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        self.model.fit(X_train, y_train)
        self.is_fitted = True

        joblib.dump(self.model, self.model_path)
        return True

    def load(self):
        if os.path.exists(self.model_path):
            self.model = joblib.load(self.model_path)
            self.is_fitted = True

    def predict_single(self, sample_dict):
        if not self.is_fitted:
            return 0.0

        X = np.array([[
            sample_dict["temperature"],
            sample_dict["vibration"],
            sample_dict["rpm"],
            sample_dict["current"],
            sample_dict["load"]
        ]])

        if hasattr(self.model, "predict_proba"):
            probs = self.model.predict_proba(X)
            return float(probs[0,1])

        return float(self.model.predict(X)[0])

    def predict_batch(self, df):
        if not self.is_fitted:
            return [0.0] * len(df)

        X = self._prepare_features(df)

        if hasattr(self.model, "predict_proba"):
            return self.model.predict_proba(X)[:, 1].tolist()

        return self.model.predict(X).tolist()
