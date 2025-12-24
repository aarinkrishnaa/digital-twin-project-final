import os
import csv
import time
import json
import threading
from datetime import datetime
import pandas as pd

from anomaly_detector import AnomalyDetector
from predictive_maintenance import PredictiveMaintenance

# CONFIG
SENSOR_FILE = os.path.join("..", "data", "sensor_data.json")
DATA_CSV = os.path.join("..", "data", "machine_live.csv")

# Create directories
os.makedirs(os.path.dirname(DATA_CSV), exist_ok=True)

# Initialize CSV with headers
if not os.path.exists(DATA_CSV):
    with open(DATA_CSV, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "temperature", "vibration", "rpm", "current", "load", "anomaly", "risk_score"])

# Initialize models
anomaly_detector = AnomalyDetector()
predictor = PredictiveMaintenance()

def append_row(row_dict):
    with open(DATA_CSV, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            row_dict.get("timestamp"),
            row_dict.get("temperature"),
            row_dict.get("vibration"),
            row_dict.get("rpm"),
            row_dict.get("current"),
            row_dict.get("load"),
            row_dict.get("anomaly"),
            row_dict.get("risk_score"),
        ])

def process_sensor_data():
    last_modified = 0
    
    while True:
        try:
            if os.path.exists(SENSOR_FILE):
                current_modified = os.path.getmtime(SENSOR_FILE)
                
                if current_modified > last_modified:
                    with open(SENSOR_FILE, 'r') as f:
                        data = json.load(f)
                    
                    # Process data
                    data_row = {
                        "timestamp": data["timestamp"],
                        "temperature": float(data["temperature"]),
                        "vibration": float(data["vibration"]),
                        "rpm": int(data["rpm"]),
                        "current": float(data["current"]),
                        "load": int(data["load"]),
                    }
                    
                    # Anomaly detection
                    features = [[data_row["temperature"], data_row["vibration"], data_row["rpm"], data_row["current"], data_row["load"]]]
                    is_anom = anomaly_detector.is_anomaly(features)
                    data_row["anomaly"] = bool(is_anom[0]) if is_anom else False
                    
                    # Risk prediction
                    risk = predictor.predict_single(data_row)
                    data_row["risk_score"] = float(risk)
                    
                    # Save to CSV
                    append_row(data_row)
                    
                    # Print status
                    status = f"Twin Updated: T={data_row['temperature']}°C V={data_row['vibration']}mm/s RPM={data_row['rpm']} Risk={risk:.2f}"
                    if data_row["anomaly"]:
                        status += "  ⚠️ ANOMALY"
                    print(status)
                    
                    last_modified = current_modified
                    
        except Exception as e:
            print("Error processing data:", e)
        
        time.sleep(1)

def main():
    print("Digital Twin Engine (File-based) running...")
    process_sensor_data()

if __name__ == "__main__":
    main()