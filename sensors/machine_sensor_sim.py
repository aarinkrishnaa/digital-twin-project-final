
import time
import json
import random
import paho.mqtt.client as mqtt

# MQTT Config
BROKER = "localhost"
TOPIC = "factory/machine1/sensors"

# Connect to MQTT broker
client = mqtt.Client()
client.connect(BROKER, 1883, 60)

def generate_sensor_data():
    """
    Generate fake sensor readings for machine
    """
    data = {
        "temperature": round(random.uniform(50, 85), 2),  # degrees Celsius
        "vibration": round(random.uniform(1, 8), 2),      # mm/s
        "rpm": random.randint(1000, 2000),                # rotations per minute
        "current": round(random.uniform(5, 15), 2),       # amperes
        "load": random.randint(50, 100)                   # percent
    }
    return data

def main():
    print("Machine Sensor Simulator running...")
    while True:
        sensor_data = generate_sensor_data()
        payload = json.dumps(sensor_data)
        client.publish(TOPIC, payload)
        print("Published:", sensor_data)
        time.sleep(1)  # 1 second interval

if __name__ == "__main__":
    main()
