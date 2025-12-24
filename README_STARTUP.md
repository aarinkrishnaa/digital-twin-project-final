# Smart Factory Digital Twin - Startup Guide

## Quick Start Options

### Option 1: Batch Script (Windows)
```bash
# Double-click or run from command line
start_all.bat
```
This will open 3 separate command windows for each component.

### Option 2: Python Startup Script
```bash
python start_system.py
```
This provides better process management and monitoring.

### Option 3: Manual Startup (Individual Components)

#### 1. Start Sensor Simulator
```bash
cd sensors
python machine_sensor_sim.py
```

#### 2. Start Twin Engine  
```bash
cd twin
python twin_engine.py
```

#### 3. Start Dashboard
```bash
cd dashboard
python app.py
```

## Access Points

- **Main Dashboard**: http://127.0.0.1:8050
- **3D Model Only**: http://127.0.0.1:8050/assets/3d.html
- **Sensor Data**: Check `data/machine_live.csv`

## System Components

1. **Sensor Simulator** (`sensors/machine_sensor_sim.py`)
   - Generates realistic machine sensor data
   - Writes to `data/machine_live.csv`
   - Updates every 2 seconds

2. **Twin Engine** (`twin/twin_engine.py`)
   - Processes sensor data
   - Runs predictive models
   - Detects anomalies

3. **Dashboard** (`dashboard/app.py`)
   - Web interface on port 8050
   - Real-time charts and 3D visualization
   - Motor control functionality

## Troubleshooting

- **Port 8050 in use**: Change port in `dashboard/app.py`
- **Missing data**: Ensure sensor simulator is running first
- **Charts not updating**: Check if all three components are running
- **Motor control not working**: Restart dashboard component

## Stopping the System

- **Batch Script**: Close all command windows
- **Python Script**: Press Ctrl+C in the main terminal
- **Manual**: Stop each component individually with Ctrl+C