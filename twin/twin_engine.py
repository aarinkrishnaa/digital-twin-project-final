# SmartFactory_DigitalTwin/twin/twin_engine.py
import os
import csv
import time
import json
import threading
from datetime import datetime

import paho.mqtt.client as mqtt
import pandas as pd

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from anomaly_detector import AnomalyDetector
from predictive_maintenance import PredictiveMaintenance

# CONFIG
BROKER = "localhost"
SENSOR_TOPIC = "factory/machine1/sensors"
DATA_CSV = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "machine_live.csv")
RETRAIN_INTERVAL_SECONDS = 60  # retrain predictor every 60s (adjustable)

# ensure data folder exists and csv header present
os.makedirs(os.path.dirname(DATA_CSV), exist_ok=True)
if not os.path.exists(DATA_CSV):
    with open(DATA_CSV, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "temperature", "vibration", "rpm", "current", "load", "anomaly", "risk_score"])

# instantiate models
anomaly_detector = AnomalyDetector()
predictor = PredictiveMaintenance()

# helper: append row to csv
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

# periodic retrain thread
def retrain_loop():
    while True:
        try:
            df = pd.read_csv(DATA_CSV)
            success = False
            if len(df) >= 30:  # need at least 30 points to train
                success = predictor.train(df)
            if success:
                print(f"[{datetime.now()}] Predictor retrained on {len(df)} samples.")
            else:
                print(f"[{datetime.now()}] Not enough data to retrain (have {len(df)} rows).")
        except Exception as e:
            print("Retrain loop error:", e)
        time.sleep(RETRAIN_INTERVAL_SECONDS)

# MQTT callbacks
def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker, subscribing to", SENSOR_TOPIC)
    client.subscribe(SENSOR_TOPIC)

def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode()
        data = json.loads(payload)
        data_row = {
            "timestamp": datetime.utcnow().isoformat(),
            "temperature": float(data.get("temperature", None)),
            "vibration": float(data.get("vibration", None)),
            "rpm": int(data.get("rpm", 0)),
            "current": float(data.get("current", None)),
            "load": int(data.get("load", 0)),
        }

        # anomaly detection
        is_anom = anomaly_detector.is_anomaly([[data_row["temperature"], data_row["vibration"], data_row["rpm"], data_row["current"], data_row["load"]]])
        data_row["anomaly"] = bool(is_anom[0])

        # risk prediction (0.0 - 1.0)
        risk = predictor.predict_single(data_row)
        data_row["risk_score"] = float(risk)

        # append to CSV
        append_row(data_row)

        # print status
        status = f"Twin Updated: T={data_row['temperature']}C V={data_row['vibration']}mm/s RPM={data_row['rpm']} Risk={risk:.2f}"
        if data_row["anomaly"]:
            status += "  ⚠️ ANOMALY"
        print(status)

        # optional: publish alerts (example topic)
        if data_row["anomaly"] or risk > 0.6:
            alert = {"timestamp": data_row["timestamp"], "anomaly": data_row["anomaly"], "risk_score": data_row["risk_score"]}
            client.publish("factory/machine1/alerts", json.dumps(alert))

    except Exception as e:
        print("Error handling message:", e)

def main():
    # start retrain thread
    t = threading.Thread(target=retrain_loop, daemon=True)
    t.start()

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(BROKER, 1883, 60)
    print("Digital Twin Engine running...")
    client.loop_forever()

if __name__ == "__main__":
    main()
