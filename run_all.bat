@echo off
echo Starting Smart Factory Digital Twin...

pip install -r requirements.txt

start python sensors/machine_sensor_sim.py
timeout /t 2
start python twin/twin_engine.py
timeout /t 2
python dashboard/app.py