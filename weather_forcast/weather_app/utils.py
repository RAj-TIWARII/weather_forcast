
import requests
from datetime import datetime
from typing import Tuple
from PIL import Image, ImageTk
from .config import OPENWEATHER_ICON_URL, ICONS_DIR, TEMP_COLOR_THEMES

def kelvin_to_celsius(kelvin: float) -> float:
    """Convert Kelvin to Celsius"""
    return kelvin - 273.15

def kelvin_to_fahrenheit(kelvin: float) -> float:
    """Convert Kelvin to Fahrenheit"""
    return (kelvin - 273.15) * 9/5 + 32

def get_temperature_color_theme(temp_celsius: float) -> dict:
    """Get color theme based on temperature"""
    if temp_celsius < 0:
        return TEMP_COLOR_THEMES["very_cold"]
    elif temp_celsius < 15:
        return TEMP_COLOR_THEMES["cold"]
    elif temp_celsius < 25:
        return TEMP_COLOR_THEMES["mild"]
    elif temp_celsius < 35:
        return TEMP_COLOR_THEMES["warm"]
    elif temp_celsius < 40:
        return TEMP_COLOR_THEMES["hot"]
    else:
        return TEMP_COLOR_THEMES["very_hot"]

def is_daytime(sunrise: int, sunset: int, current_time: int = None) -> bool:
    """Check if it's currently daytime"""
    if current_time is None:
        current_time = int(datetime.now().timestamp())
    return sunrise <= current_time <= sunset

def download_weather_icon(icon_code: str, size: str = "@2x") -> str:
    """
    Download weather icon from OpenWeatherMap

    Args:
        icon_code: Icon code from API response
        size: Icon size (@2x for larger icons)

    Returns:
        Path to downloaded icon file
    """
    icon_filename = f"{icon_code}{size}.png"
    icon_path = ICONS_DIR / icon_filename

    # Return existing file if already downloaded
    if icon_path.exists():
        return str(icon_path)

    try:
        icon_url = f"{OPENWEATHER_ICON_URL}{icon_filename}"
        response = requests.get(icon_url, timeout=10)
        response.raise_for_status()

        with open(icon_path, 'wb') as f:
            f.write(response.content)

        return str(icon_path)

    except requests.exceptions.RequestException as e:
        print(f"Error downloading icon: {e}")
        return ""

def load_and_resize_image(image_path: str, size: Tuple[int, int]) -> ImageTk.PhotoImage:
    """
    Load and resize an image for tkinter

    Args:
        image_path: Path to image file
        size: Desired size as (width, height)

    Returns:
        PhotoImage object for tkinter
    """
    try:
        image = Image.open(image_path)
        image = image.resize(size, Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(image)
    except Exception as e:
        print(f"Error loading image {image_path}: {e}")
        # Return a default placeholder image
        placeholder = Image.new('RGB', size, color='lightgray')
        return ImageTk.PhotoImage(placeholder)

def format_timestamp(timestamp: int, format_str: str = "%H:%M") -> str:
    """Format unix timestamp to readable time"""
    return datetime.fromtimestamp(timestamp).strftime(format_str)

def get_wind_direction(degrees: float) -> str:
    """Convert wind degrees to cardinal direction"""
    directions = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
                  "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
    index = round(degrees / 22.5) % 16
    return directions[index]

def get_weather_emoji(weather_main: str, icon_code: str = "") -> str:
    """Get emoji representation of weather condition"""
    weather_emojis = {
        "Clear": "☀️" if "d" in icon_code else "🌙",
        "Clouds": "☁️",
        "Rain": "🌧️",
        "Drizzle": "🌦️",
        "Thunderstorm": "⛈️",
        "Snow": "❄️",
        "Mist": "🌫️",
        "Fog": "🌫️",
        "Haze": "🌫️",
        "Dust": "🌪️",
        "Sand": "🌪️",
        "Ash": "🌋",
        "Squall": "💨",
        "Tornado": "🌪️"
    }
    return weather_emojis.get(weather_main, "🌤️")
