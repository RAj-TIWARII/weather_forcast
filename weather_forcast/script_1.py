# Create a comprehensive setup and installation guide
setup_guide = """
# 🌤️ WeatherPy Advanced - Complete Setup Guide

## 📋 Project Overview

WeatherPy Advanced is a modern, feature-rich weather application built with Python and CustomTkinter. It provides:

✅ **Real-time weather data** for any city worldwide
✅ **5-day detailed forecasts** with daily highs and lows
✅ **Modern responsive UI** with CustomTkinter
✅ **Dynamic themes** that change based on temperature
✅ **Smart city search** with autocomplete
✅ **Auto-refresh functionality** every 5 minutes
✅ **Customizable settings** for units and preferences
✅ **Custom weather icons** and beautiful backgrounds

## 🚀 Quick Start

### Step 1: Download and Extract
1. Download the complete project folder
2. Extract to your desired location
3. Open terminal/command prompt in the project folder

### Step 2: Get API Key (FREE)
1. Visit https://openweathermap.org/api
2. Sign up for a free account
3. Go to "API Keys" section
4. Copy your API key

### Step 3: Configure API Key
1. Open `weather_app/config.py`
2. Replace `"your_api_key_here"` with your actual API key:
   ```python
   OPENWEATHER_API_KEY = "your_actual_api_key_here"
   ```

### Step 4: Setup Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\\Scripts\\activate
# On macOS/Linux:
source venv/bin/activate
```

### Step 5: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 6: Run the Application
```bash
# Method 1: Using the launcher
python run_app.py

# Method 2: Direct execution
python -m weather_app.main_app
```

## 📁 Project Structure

```
weatherpy_advanced/
├── 🐍 run_app.py              # Easy launcher script
├── 📄 requirements.txt        # Python dependencies
├── 📖 README.md              # Documentation
├── ⚙️ setup.py               # Package installation
├── 🙈 .gitignore             # Git ignore rules
└── 📦 weather_app/           # Main application package
    ├── 🔧 __init__.py        # Package initializer
    ├── ⚙️ config.py          # Configuration settings
    ├── 🌐 api_client.py      # Weather API client
    ├── 🛠️ utils.py           # Utility functions
    ├── 🎨 widgets.py         # Custom UI components
    ├── 🖥️ main_app.py        # Main application
    ├── 📁 assets/            # Images and icons
    │   ├── 🎨 icons/         # Weather icons
    │   └── 🖼️ backgrounds/   # Weather backgrounds
    └── 💾 cache/             # API response cache
```

## 🎨 Features Overview

### 🔍 Smart Search
- Type any city name worldwide
- Autocomplete suggestions
- Error handling for invalid cities

### 🌡️ Current Weather Display
- **Large temperature display** with dynamic color themes
- **Weather condition** with emoji icons
- **Detailed information cards**:
  - 💧 Humidity levels
  - 💨 Wind speed and direction
  - 🌡️ Atmospheric pressure
  - 👁️ Visibility distance
  - 🌅 Sunrise time
  - 🌇 Sunset time
  - ☁️ Cloud coverage

### 📅 5-Day Forecast
- Daily high and low temperatures
- Weather condition icons
- Brief descriptions
- Easy-to-read cards layout

### ⚙️ Customizable Settings
- **Temperature Units**: Celsius, Fahrenheit, or Kelvin
- **Auto-refresh**: Enable/disable automatic updates
- **Theme Selection**: Dark, Light, or System theme

### 🎨 Dynamic Theming
The app automatically changes color themes based on temperature:
- ❄️ **Very Cold** (< 0°C): Blue theme
- 🧊 **Cold** (0-15°C): Light blue theme  
- 🌿 **Mild** (15-25°C): Green theme
- ☀️ **Warm** (25-35°C): Yellow theme
- 🔥 **Hot** (35-40°C): Orange theme
- 🌋 **Very Hot** (> 40°C): Red theme

## 🛠️ Customization

### Adding Your Own Icons
1. Place icon files in `weather_app/assets/icons/`
2. Update icon mappings in `utils.py`
3. Supported formats: PNG, JPG, ICO

### Custom Background Images
1. Add images to `weather_app/assets/backgrounds/`
2. Update `WEATHER_BACKGROUNDS` in `config.py`
3. Name format: `condition_timeofday.jpg`

### Modifying Color Themes
Edit `TEMP_COLOR_THEMES` in `config.py`:
```python
TEMP_COLOR_THEMES = {
    "your_theme": {
        "bg": "#HEX_COLOR",
        "text": "#HEX_COLOR", 
        "accent": "#HEX_COLOR"
    }
}
```

## 🔧 Troubleshooting

### Common Issues

**❌ "Module not found" errors**
```bash
# Make sure virtual environment is activated
pip install -r requirements.txt
```

**❌ "API key invalid" error**
- Double-check your API key in `config.py`
- Ensure no extra spaces or quotes
- Verify your OpenWeatherMap account is active

**❌ "City not found" error**
- Check spelling of city name
- Try different variations (e.g., "New York, NY")
- Some cities need country codes

**❌ App won't start**
```bash
# Check Python version (3.8+ required)
python --version

# Reinstall dependencies
pip uninstall -r requirements.txt -y
pip install -r requirements.txt
```

### Performance Tips

🚀 **Faster loading**:
- API responses are cached for 10 minutes
- Icons are downloaded once and cached locally
- Auto-refresh can be disabled in settings

💾 **Memory usage**:
- Cache is automatically cleaned
- Old icons are periodically removed
- Minimal background processes

## 🌐 API Information

### OpenWeatherMap API Limits (Free Tier)
- ✅ **60 calls per minute**
- ✅ **1,000 calls per day**
- ✅ **Current weather data**
- ✅ **5-day/3-hour forecast**
- ✅ **Weather icons**

### Supported Weather Data
- 🌡️ Temperature (current, feels like, min/max)
- 💧 Humidity percentage
- 💨 Wind speed and direction
- 🌡️ Atmospheric pressure
- 👁️ Visibility distance
- ☁️ Cloud coverage percentage
- 🌅 Sunrise and sunset times
- 🏙️ City and country information

## 📱 Planned Features

🔮 **Coming Soon**:
- [ ] Weather alerts and notifications
- [ ] GPS-based location detection
- [ ] Weather maps and radar
- [ ] Multiple favorite cities
- [ ] Historical weather charts
- [ ] Export weather reports
- [ ] Weather widgets for desktop

## 🤝 Contributing

Want to help improve WeatherPy Advanced?

1. **Fork** the repository
2. **Create** a feature branch
3. **Make** your improvements
4. **Test** thoroughly
5. **Submit** a pull request

### Development Setup
```bash
# Clone your fork
git clone https://github.com/yourusername/weatherpy.git

# Install development dependencies
pip install -r requirements.txt
pip install pytest black flake8 mypy

# Run tests
pytest

# Format code
black weather_app/
```

## 📞 Support

**Need help?**
- 📖 Check this setup guide first
- 🐛 Report bugs via GitHub Issues
- 💡 Suggest features via GitHub Discussions
- 📧 Contact maintainer for urgent issues

## 🎉 Enjoy!

You now have a fully functional, modern weather application! 

**Pro Tips**:
- Try searching for cities around the world
- Watch the themes change with temperature
- Customize the settings to your preference
- Add your own weather icons for a personal touch

Happy weather tracking! 🌤️
"""

# Save the setup guide
with open("weatherpy_advanced/SETUP_GUIDE.md", "w", encoding="utf-8") as f:
    f.write(setup_guide)

print("📖 Created comprehensive setup guide: SETUP_GUIDE.md")

# Create a simple batch file for Windows users
windows_launcher = """@echo off
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
call venv\\Scripts\\activate

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
"""

with open("weatherpy_advanced/start_app.bat", "w", encoding="utf-8") as f:
    f.write(windows_launcher)

print("🪟 Created Windows launcher: start_app.bat")

# Create a shell script for Linux/Mac users
unix_launcher = """#!/bin/bash

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
"""

with open("weatherpy_advanced/start_app.sh", "w", encoding="utf-8") as f:
    f.write(unix_launcher)

# Make the shell script executable
import os
os.chmod("weatherpy_advanced/start_app.sh", 0o755)

print("🐧 Created Linux/Mac launcher: start_app.sh")

# Create a final project summary
project_summary = """
🎉 WEATHERPY ADVANCED - COMPLETE PROJECT READY! 🎉

📁 Project Structure Created:
   ✅ Complete Python package structure
   ✅ Modern CustomTkinter UI
   ✅ OpenWeatherMap API integration
   ✅ Dynamic themes and backgrounds
   ✅ Custom weather icons support
   ✅ Comprehensive documentation
   ✅ Cross-platform launchers

🚀 What's Included:
   📱 Modern responsive GUI with CustomTkinter
   🌡️ Real-time weather data for any city
   📅 5-day detailed weather forecasts  
   🎨 Dynamic color themes based on temperature
   🔍 Smart city search with error handling
   ⚙️ Customizable settings panel
   🔄 Auto-refresh functionality
   💾 API response caching
   🖼️ Custom icon and background support
   📖 Complete documentation and setup guides

🛠️ Technologies Used:
   🐍 Python 3.8+
   🎨 CustomTkinter (modern UI)
   🖼️ Pillow (image processing)
   🌐 Requests (API calls)
   ☁️ OpenWeatherMap API
   
📋 Ready to Use:
   1. Get free API key from OpenWeatherMap
   2. Edit config.py with your API key
   3. Run start_app.bat (Windows) or start_app.sh (Linux/Mac)
   4. Enjoy your professional weather app!

🎯 Perfect for:
   ✨ Learning GUI development
   ✨ API integration projects
   ✨ Portfolio demonstrations
   ✨ Daily weather tracking
   ✨ Python skill building

Your advanced weather application is ready to use! 🌤️
"""

print(project_summary)