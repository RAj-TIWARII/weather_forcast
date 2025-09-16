
# Configuration file for Weather App
import os
from pathlib import Path

# API Configuration
OPENWEATHER_API_KEY = "paste_your_api_key"  # Get from https://openweathermap.org/api
OPENWEATHER_BASE_URL = "http://api.openweathermap.org/data/2.5/"
OPENWEATHER_ICON_URL = "http://openweathermap.org/img/wn/"

# App Configuration
APP_NAME = "Weather forcast"
APP_VERSION = "1.0.0"
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
WINDOW_MIN_WIDTH = 800
WINDOW_MIN_HEIGHT = 600

# Paths
BASE_DIR = Path(__file__).parent
ASSETS_DIR = BASE_DIR / "assets"
ICONS_DIR = ASSETS_DIR / "icons"
BACKGROUNDS_DIR = ASSETS_DIR / "backgrounds"
CACHE_DIR = BASE_DIR / "cache"

# Create directories if they don't exist
for directory in [ASSETS_DIR, ICONS_DIR, BACKGROUNDS_DIR, CACHE_DIR]:
    directory.mkdir(exist_ok=True)

# Weather condition mappings for backgrounds
WEATHER_BACKGROUNDS = {
    "clear": {
        "day": "clear_day.jpg",
        "night": "clear_night.jpg"
    },
    "clouds": {
        "day": "cloudy_day.jpg", 
        "night": "cloudy_night.jpg"
    },
    "rain": {
        "day": "rainy_day.jpg",
        "night": "rainy_night.jpg"
    },
    "drizzle": {
        "day": "drizzle_day.jpg",
        "night": "drizzle_night.jpg"
    },
    "thunderstorm": {
        "day": "thunderstorm_day.jpg",
        "night": "thunderstorm_night.jpg"
    },
    "snow": {
        "day": "snow_day.jpg",
        "night": "snow_night.jpg"
    },
    "mist": {
        "day": "mist_day.jpg",
        "night": "mist_night.jpg"
    },
    "fog": {
        "day": "fog_day.jpg",
        "night": "fog_night.jpg"
    },
    "default": {
        "day": "default_day.jpg",
        "night": "default_night.jpg"
    }
}

# Color themes based on temperature
TEMP_COLOR_THEMES = {
    "very_cold": {"bg": "#2C5AA0", "text": "#FFFFFF", "accent": "#4A90E2"},  # Blue theme for < 0°C
    "cold": {"bg": "#5DADE2", "text": "#2C3E50", "accent": "#3498DB"},      # Light blue for 0-15°C
    "mild": {"bg": "#58D68D", "text": "#2C3E50", "accent": "#27AE60"},      # Green for 15-25°C
    "warm": {"bg": "#F7DC6F", "text": "#2C3E50", "accent": "#F39C12"},      # Yellow for 25-35°C
    "hot": {"bg": "#E67E22", "text": "#FFFFFF", "accent": "#D35400"},       # Orange for 35-40°C
    "very_hot": {"bg": "#E74C3C", "text": "#FFFFFF", "accent": "#C0392B"}    # Red for > 40°C
}

# Default settings
DEFAULT_CITY = "London"
DEFAULT_UNITS = "metric"  # metric, imperial, kelvin
REFRESH_INTERVAL = 300000  # 5 minutes in milliseconds
CACHE_DURATION = 600  # 10 minutes in seconds
