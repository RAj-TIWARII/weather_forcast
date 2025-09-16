@echo off
title WeatherPy Advanced - Weather Forecast Application
echo.
echo 🌤️  WeatherPy Advanced - Starting up...
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ❌ Failed to create virtual environment
        echo 💡 Make sure Python 3.8+ is installed
        pause
        exit /b 1
    )
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate

REM Install dependencies if needed
echo 📦 Checking dependencies...
pip install -r requirements.txt >nul 2>&1

REM Launch the application
echo 🚀 Starting WeatherPy Advanced...
echo.
python run_app.py

echo.
echo 👋 Thanks for using WeatherPy Advanced!
pause
