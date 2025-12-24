import subprocess
import time
import os
import sys

def start_component(name, script_path, working_dir):
    """Start a component in a new process"""
    try:
        print(f"Starting {name}...")
        
        # Change to the working directory and run the script
        process = subprocess.Popen([
            sys.executable, script_path
        ], cwd=working_dir, creationflags=subprocess.CREATE_NEW_CONSOLE)
        
        print(f"✓ {name} started (PID: {process.pid})")
        return process
    except Exception as e:
        print(f"✗ Failed to start {name}: {e}")
        return None

def main():
    print("=" * 60)
    print("SMART FACTORY DIGITAL TWIN - SYSTEM STARTUP")
    print("=" * 60)
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    processes = []
    
    # Start Sensor Simulator
    sensor_process = start_component(
        "Sensor Simulator",
        "machine_sensor_sim.py",
        os.path.join(base_dir, "sensors")
    )
    if sensor_process:
        processes.append(("Sensor Simulator", sensor_process))
    
    time.sleep(2)
    
    # Start Twin Engine
    twin_process = start_component(
        "Twin Engine",
        "twin_engine.py", 
        os.path.join(base_dir, "twin")
    )
    if twin_process:
        processes.append(("Twin Engine", twin_process))
    
    time.sleep(2)
    
    # Start Dashboard
    dashboard_process = start_component(
        "Dashboard",
        "app.py",
        os.path.join(base_dir, "dashboard")
    )
    if dashboard_process:
        processes.append(("Dashboard", dashboard_process))
    
    print("\n" + "=" * 60)
    print("SYSTEM STATUS")
    print("=" * 60)
    
    for name, process in processes:
        status = "RUNNING" if process.poll() is None else "STOPPED"
        print(f"{name}: {status}")
    
    print("\n📊 Dashboard URL: http://127.0.0.1:8050")
    print("🔧 3D Model URL: http://127.0.0.1:8050/assets/3d.html")
    
    print("\nPress Ctrl+C to stop all components...")
    
    try:
        # Keep the script running
        while True:
            time.sleep(5)
            # Check if any process has died
            for name, process in processes:
                if process.poll() is not None:
                    print(f"⚠️  {name} has stopped unexpectedly")
    except KeyboardInterrupt:
        print("\n\nShutting down all components...")
        for name, process in processes:
            try:
                process.terminate()
                print(f"✓ {name} stopped")
            except:
                print(f"✗ Failed to stop {name}")
        print("System shutdown complete.")

if __name__ == "__main__":
    main()