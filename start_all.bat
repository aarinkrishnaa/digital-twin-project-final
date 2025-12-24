@echo off
echo Starting Smart Factory Digital Twin System...
echo.

REM Create new command windows for each component
echo Starting Sensor Simulator...
start "Sensor Simulator" cmd /k "cd /d sensors && python machine_sensor_sim.py"

timeout /t 3 /nobreak >nul

echo Starting Twin Engine...
start "Twin Engine" cmd /k "cd /d twin && python twin_engine.py"

timeout /t 3 /nobreak >nul

echo Starting Dashboard...
start "Dashboard" cmd /k "cd /d dashboard && python app.py"

echo.
echo All components started!
echo - Sensor Simulator: Running in separate window
echo - Twin Engine: Running in separate window  
echo - Dashboard: Running in separate window
echo.
echo Dashboard will be available at: http://127.0.0.1:8050
echo.
pause