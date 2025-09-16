#!/bin/bash

echo "🌤️  WeatherPy Advanced - Starting up..."
echo

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "❌ Failed to create virtual environment"
        echo "💡 Make sure Python 3.8+ is installed"
        exit 1
    fi
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies if needed
echo "📦 Checking dependencies..."
pip install -r requirements.txt > /dev/null 2>&1

# Launch the application
echo "🚀 Starting WeatherPy Advanced..."
echo
python run_app.py

echo
echo "👋 Thanks for using WeatherPy Advanced!"
