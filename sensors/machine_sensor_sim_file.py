import time
import json
import random
import csv
import os
from datetime import datetime

DATA_FILE = os.path.join("..", "data", "sensor_data.json")

def generate_sensor_data():
    return {
        "timestamp": datetime.now().isoformat(),
        "temperature": round(random.uniform(50, 85), 2),
        "vibration": round(random.uniform(1, 8), 2),
        "rpm": random.randint(1000, 2000),
        "current": round(random.uniform(5, 15), 2),
        "load": random.randint(50, 100)
    }

def main():
    print("Machine Sensor Simulator (File-based) running...")
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    
    while True:
        sensor_data = generate_sensor_data()
        
        # Write to JSON file
        with open(DATA_FILE, 'w') as f:
            json.dump(sensor_data, f)
        
        print("Generated:", sensor_data)
        time.sleep(2)

if __name__ == "__main__":
    main()