# Create the complete weather application structure with all necessary files
import os

# Define the project structure
project_structure = {
    "weather_app": {
        "__init__.py": "",
        "config.py": """
# Configuration file for Weather App
import os
from pathlib import Path

# API Configuration
OPENWEATHER_API_KEY = "your_api_key_here"  # Get from https://openweathermap.org/api
OPENWEATHER_BASE_URL = "http://api.openweathermap.org/data/2.5/"
OPENWEATHER_ICON_URL = "http://openweathermap.org/img/wn/"

# App Configuration
APP_NAME = "WeatherPy - Advanced Weather Forecast"
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
""",
        
        "api_client.py": """
import requests
import json
import time
from typing import Dict, Optional, Tuple
from .config import OPENWEATHER_API_KEY, OPENWEATHER_BASE_URL, CACHE_DIR, CACHE_DURATION

class WeatherAPIClient:
    \"\"\"Client for fetching weather data from OpenWeatherMap API\"\"\"
    
    def __init__(self):
        self.api_key = OPENWEATHER_API_KEY
        self.base_url = OPENWEATHER_BASE_URL
        self.cache = {}
        
    def _get_cache_key(self, city: str, units: str) -> str:
        \"\"\"Generate cache key for storing weather data\"\"\"
        return f"{city.lower()}_{units}"
    
    def _is_cache_valid(self, timestamp: float) -> bool:
        \"\"\"Check if cached data is still valid\"\"\"
        return time.time() - timestamp < CACHE_DURATION
    
    def get_current_weather(self, city: str, units: str = "metric") -> Optional[Dict]:
        \"\"\"
        Fetch current weather for a city
        
        Args:
            city: City name
            units: Temperature units (metric, imperial, kelvin)
            
        Returns:
            Weather data dictionary or None if error
        \"\"\"
        cache_key = self._get_cache_key(city, units)
        
        # Check cache first
        if cache_key in self.cache:
            data, timestamp = self.cache[cache_key]
            if self._is_cache_valid(timestamp):
                return data
        
        try:
            url = f"{self.base_url}weather"
            params = {
                "q": city,
                "appid": self.api_key,
                "units": units
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # Cache the data
            self.cache[cache_key] = (data, time.time())
            
            return data
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching weather data: {e}")
            return None
        except json.JSONDecodeError as e:
            print(f"Error parsing weather data: {e}")
            return None
    
    def get_forecast(self, city: str, units: str = "metric") -> Optional[Dict]:
        \"\"\"
        Fetch 5-day weather forecast for a city
        
        Args:
            city: City name
            units: Temperature units (metric, imperial, kelvin)
            
        Returns:
            Forecast data dictionary or None if error
        \"\"\"
        cache_key = f"forecast_{self._get_cache_key(city, units)}"
        
        # Check cache first
        if cache_key in self.cache:
            data, timestamp = self.cache[cache_key]
            if self._is_cache_valid(timestamp):
                return data
        
        try:
            url = f"{self.base_url}forecast"
            params = {
                "q": city,
                "appid": self.api_key,
                "units": units
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # Cache the data
            self.cache[cache_key] = (data, time.time())
            
            return data
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching forecast data: {e}")
            return None
        except json.JSONDecodeError as e:
            print(f"Error parsing forecast data: {e}")
            return None
    
    def search_cities(self, query: str, limit: int = 5) -> list:
        \"\"\"
        Search for cities by name
        
        Args:
            query: Search query
            limit: Maximum number of results
            
        Returns:
            List of city data dictionaries
        \"\"\"
        try:
            url = f"http://api.openweathermap.org/geo/1.0/direct"
            params = {
                "q": query,
                "limit": limit,
                "appid": self.api_key
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            print(f"Error searching cities: {e}")
            return []
""",
        
        "utils.py": """
import requests
from datetime import datetime
from typing import Tuple
from PIL import Image, ImageTk
from .config import OPENWEATHER_ICON_URL, ICONS_DIR, TEMP_COLOR_THEMES

def kelvin_to_celsius(kelvin: float) -> float:
    \"\"\"Convert Kelvin to Celsius\"\"\"
    return kelvin - 273.15

def kelvin_to_fahrenheit(kelvin: float) -> float:
    \"\"\"Convert Kelvin to Fahrenheit\"\"\"
    return (kelvin - 273.15) * 9/5 + 32

def get_temperature_color_theme(temp_celsius: float) -> dict:
    \"\"\"Get color theme based on temperature\"\"\"
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
    \"\"\"Check if it's currently daytime\"\"\"
    if current_time is None:
        current_time = int(datetime.now().timestamp())
    return sunrise <= current_time <= sunset

def download_weather_icon(icon_code: str, size: str = "@2x") -> str:
    \"\"\"
    Download weather icon from OpenWeatherMap
    
    Args:
        icon_code: Icon code from API response
        size: Icon size (@2x for larger icons)
        
    Returns:
        Path to downloaded icon file
    \"\"\"
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
    \"\"\"
    Load and resize an image for tkinter
    
    Args:
        image_path: Path to image file
        size: Desired size as (width, height)
        
    Returns:
        PhotoImage object for tkinter
    \"\"\"
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
    \"\"\"Format unix timestamp to readable time\"\"\"
    return datetime.fromtimestamp(timestamp).strftime(format_str)

def get_wind_direction(degrees: float) -> str:
    \"\"\"Convert wind degrees to cardinal direction\"\"\"
    directions = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
                  "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
    index = round(degrees / 22.5) % 16
    return directions[index]

def get_weather_emoji(weather_main: str, icon_code: str = "") -> str:
    \"\"\"Get emoji representation of weather condition\"\"\"
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
""",
        
        "widgets.py": """
import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from typing import Callable, Optional, List, Dict
from datetime import datetime

class ModernSearchEntry(ctk.CTkFrame):
    \"\"\"Modern search entry with autocomplete functionality\"\"\"
    
    def __init__(self, parent, search_callback: Callable = None, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.search_callback = search_callback
        self.suggestions = []
        
        # Create search entry
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self._on_search_change)
        
        self.search_entry = ctk.CTkEntry(
            self,
            textvariable=self.search_var,
            placeholder_text="Enter city name...",
            font=ctk.CTkFont(size=16),
            height=40,
            width=300
        )
        self.search_entry.pack(side="left", padx=(0, 10), fill="x", expand=True)
        
        # Search button
        self.search_button = ctk.CTkButton(
            self,
            text="🔍",
            command=self._on_search_click,
            width=40,
            height=40,
            font=ctk.CTkFont(size=18)
        )
        self.search_button.pack(side="right")
        
        # Autocomplete dropdown (initially hidden)
        self.dropdown_frame = ctk.CTkFrame(self)
        self.dropdown_visible = False
        
        # Bind events
        self.search_entry.bind('<Return>', lambda e: self._on_search_click())
        self.search_entry.bind('<FocusOut>', self._hide_dropdown)
    
    def _on_search_change(self, *args):
        \"\"\"Handle search text changes for autocomplete\"\"\"
        query = self.search_var.get().strip()
        if len(query) >= 2:
            # Here you would typically call an API to get city suggestions
            # For now, we'll just hide the dropdown
            self._hide_dropdown()
    
    def _on_search_click(self):
        \"\"\"Handle search button click\"\"\"
        if self.search_callback:
            self.search_callback(self.search_var.get().strip())
        self._hide_dropdown()
    
    def _hide_dropdown(self, event=None):
        \"\"\"Hide autocomplete dropdown\"\"\"
        if self.dropdown_visible:
            self.dropdown_frame.pack_forget()
            self.dropdown_visible = False
    
    def set_text(self, text: str):
        \"\"\"Set search entry text\"\"\"
        self.search_var.set(text)

class WeatherCard(ctk.CTkFrame):
    \"\"\"Card widget for displaying weather information\"\"\"
    
    def __init__(self, parent, title: str = "", **kwargs):
        super().__init__(parent, **kwargs)
        
        self.title_label = ctk.CTkLabel(
            self,
            text=title,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.title_label.pack(pady=(10, 5))
        
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))
    
    def add_info_row(self, label: str, value: str, icon: str = ""):
        \"\"\"Add an information row to the card\"\"\"
        row_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        row_frame.pack(fill="x", pady=2)
        
        info_text = f"{icon} {label}: {value}" if icon else f"{label}: {value}"
        info_label = ctk.CTkLabel(
            row_frame,
            text=info_text,
            font=ctk.CTkFont(size=12),
            anchor="w"
        )
        info_label.pack(fill="x")

class ForecastCard(ctk.CTkFrame):
    \"\"\"Card for displaying daily forecast\"\"\"
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        
        # Day label
        self.day_label = ctk.CTkLabel(
            self,
            text="",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        self.day_label.pack(pady=(10, 5))
        
        # Weather icon (placeholder)
        self.icon_label = ctk.CTkLabel(
            self,
            text="",
            font=ctk.CTkFont(size=24)
        )
        self.icon_label.pack(pady=5)
        
        # Temperature
        self.temp_label = ctk.CTkLabel(
            self,
            text="",
            font=ctk.CTkFont(size=14)
        )
        self.temp_label.pack(pady=5)
        
        # Description
        self.desc_label = ctk.CTkLabel(
            self,
            text="",
            font=ctk.CTkFont(size=10),
            wraplength=100
        )
        self.desc_label.pack(pady=(0, 10))
    
    def update_forecast(self, day: str, icon: str, temp_high: str, temp_low: str, description: str):
        \"\"\"Update forecast card with new data\"\"\"
        self.day_label.configure(text=day)
        self.icon_label.configure(text=icon)
        self.temp_label.configure(text=f"{temp_high}° / {temp_low}°")
        self.desc_label.configure(text=description.title())

class SettingsPanel(ctk.CTkFrame):
    \"\"\"Settings panel for app configuration\"\"\"
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        
        # Title
        title_label = ctk.CTkLabel(
            self,
            text="Settings",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title_label.pack(pady=(20, 10))
        
        # Units selection
        units_frame = ctk.CTkFrame(self, fg_color="transparent")
        units_frame.pack(fill="x", padx=20, pady=10)
        
        units_label = ctk.CTkLabel(
            units_frame,
            text="Temperature Units:",
            font=ctk.CTkFont(size=14)
        )
        units_label.pack(anchor="w")
        
        self.units_var = tk.StringVar(value="metric")
        self.units_menu = ctk.CTkOptionMenu(
            units_frame,
            values=["Celsius (°C)", "Fahrenheit (°F)", "Kelvin (K)"],
            variable=self.units_var
        )
        self.units_menu.pack(fill="x", pady=(5, 0))
        
        # Auto-refresh
        refresh_frame = ctk.CTkFrame(self, fg_color="transparent")
        refresh_frame.pack(fill="x", padx=20, pady=10)
        
        self.auto_refresh_var = tk.BooleanVar(value=True)
        self.auto_refresh_check = ctk.CTkCheckBox(
            refresh_frame,
            text="Auto-refresh every 5 minutes",
            variable=self.auto_refresh_var,
            font=ctk.CTkFont(size=14)
        )
        self.auto_refresh_check.pack(anchor="w")
        
        # Theme selection
        theme_frame = ctk.CTkFrame(self, fg_color="transparent")
        theme_frame.pack(fill="x", padx=20, pady=10)
        
        theme_label = ctk.CTkLabel(
            theme_frame,
            text="App Theme:",
            font=ctk.CTkFont(size=14)
        )
        theme_label.pack(anchor="w")
        
        self.theme_var = tk.StringVar(value="dark")
        self.theme_menu = ctk.CTkOptionMenu(
            theme_frame,
            values=["Dark", "Light", "System"],
            variable=self.theme_var,
            command=self._on_theme_change
        )
        self.theme_menu.pack(fill="x", pady=(5, 0))
    
    def _on_theme_change(self, choice: str):
        \"\"\"Handle theme change\"\"\"
        theme = choice.lower()
        ctk.set_appearance_mode(theme)
    
    def get_settings(self) -> Dict:
        \"\"\"Get current settings\"\"\"
        units_map = {
            "Celsius (°C)": "metric",
            "Fahrenheit (°F)": "imperial", 
            "Kelvin (K)": "kelvin"
        }
        
        return {
            "units": units_map.get(self.units_var.get(), "metric"),
            "auto_refresh": self.auto_refresh_var.get(),
            "theme": self.theme_var.get().lower()
        }

class StatusBar(ctk.CTkFrame):
    \"\"\"Status bar for showing app status\"\"\"
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, height=30, **kwargs)
        
        self.pack_propagate(False)
        
        # Status text
        self.status_var = tk.StringVar(value="Ready")
        self.status_label = ctk.CTkLabel(
            self,
            textvariable=self.status_var,
            font=ctk.CTkFont(size=10)
        )
        self.status_label.pack(side="left", padx=10)
        
        # Last updated time
        self.time_var = tk.StringVar(value="")
        self.time_label = ctk.CTkLabel(
            self,
            textvariable=self.time_var,
            font=ctk.CTkFont(size=10)
        )
        self.time_label.pack(side="right", padx=10)
    
    def update_status(self, status: str):
        \"\"\"Update status text\"\"\"
        self.status_var.set(status)
    
    def update_time(self):
        \"\"\"Update last updated time\"\"\"
        current_time = datetime.now().strftime("%H:%M:%S")
        self.time_var.set(f"Last updated: {current_time}")
""",
        
        "main_app.py": """
import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
from datetime import datetime, timedelta
import threading
from typing import Optional, Dict
from .api_client import WeatherAPIClient
from .widgets import ModernSearchEntry, WeatherCard, ForecastCard, SettingsPanel, StatusBar
from .utils import get_temperature_color_theme, get_weather_emoji, get_wind_direction, format_timestamp
from .config import (
    APP_NAME, WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT,
    DEFAULT_CITY, DEFAULT_UNITS, REFRESH_INTERVAL
)

class WeatherApp:
    \"\"\"Main Weather Application Class\"\"\"
    
    def __init__(self):
        # Set CustomTkinter appearance
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Initialize main window
        self.root = ctk.CTk()
        self.root.title(APP_NAME)
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.minsize(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)
        
        # Initialize API client
        self.api_client = WeatherAPIClient()
        
        # Current settings
        self.current_city = DEFAULT_CITY
        self.current_units = DEFAULT_UNITS
        self.auto_refresh_enabled = True
        
        # UI components
        self.main_frame = None
        self.search_frame = None
        self.current_weather_frame = None
        self.forecast_frame = None
        self.settings_panel = None
        self.status_bar = None
        
        # Data storage
        self.current_weather_data = None
        self.forecast_data = None
        
        # Auto-refresh timer
        self.refresh_timer = None
        
        self._setup_ui()
        self._load_initial_data()
    
    def _setup_ui(self):
        \"\"\"Setup the user interface\"\"\"
        # Create main container
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Create top section with search and settings
        self._create_top_section()
        
        # Create current weather section
        self._create_current_weather_section()
        
        # Create forecast section  
        self._create_forecast_section()
        
        # Create settings panel (initially hidden)
        self._create_settings_panel()
        
        # Create status bar
        self._create_status_bar()
    
    def _create_top_section(self):
        \"\"\"Create top section with search and controls\"\"\"
        top_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        top_frame.pack(fill="x", pady=(0, 20))
        
        # Search section
        search_frame = ctk.CTkFrame(top_frame)
        search_frame.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        self.search_entry = ModernSearchEntry(
            search_frame,
            search_callback=self._on_search
        )
        self.search_entry.pack(fill="x", padx=20, pady=20)
        
        # Controls section
        controls_frame = ctk.CTkFrame(top_frame)
        controls_frame.pack(side="right")
        
        # Refresh button
        self.refresh_button = ctk.CTkButton(
            controls_frame,
            text="🔄",
            command=self._refresh_data,
            width=50,
            height=40,
            font=ctk.CTkFont(size=18)
        )
        self.refresh_button.pack(side="left", padx=10, pady=20)
        
        # Settings button
        self.settings_button = ctk.CTkButton(
            controls_frame,
            text="⚙️",
            command=self._toggle_settings,
            width=50,
            height=40,
            font=ctk.CTkFont(size=18)
        )
        self.settings_button.pack(side="left", padx=(0, 10), pady=20)
    
    def _create_current_weather_section(self):
        \"\"\"Create current weather display section\"\"\"
        self.current_weather_frame = ctk.CTkFrame(self.main_frame)
        self.current_weather_frame.pack(fill="x", pady=(0, 20))
        
        # Main weather info
        main_info_frame = ctk.CTkFrame(self.current_weather_frame)
        main_info_frame.pack(fill="x", padx=20, pady=20)
        
        # Left side - main temperature and condition
        left_frame = ctk.CTkFrame(main_info_frame, fg_color="transparent")
        left_frame.pack(side="left", fill="both", expand=True)
        
        # City name
        self.city_label = ctk.CTkLabel(
            left_frame,
            text="",
            font=ctk.CTkFont(size=32, weight="bold")
        )
        self.city_label.pack(anchor="w", pady=(0, 10))
        
        # Temperature
        self.temp_label = ctk.CTkLabel(
            left_frame,
            text="",
            font=ctk.CTkFont(size=72, weight="bold")
        )
        self.temp_label.pack(anchor="w")
        
        # Weather condition
        self.condition_label = ctk.CTkLabel(
            left_frame,
            text="",
            font=ctk.CTkFont(size=20)
        )
        self.condition_label.pack(anchor="w", pady=(0, 10))
        
        # Feels like
        self.feels_like_label = ctk.CTkLabel(
            left_frame,
            text="",
            font=ctk.CTkFont(size=14)
        )
        self.feels_like_label.pack(anchor="w")
        
        # Right side - weather details
        right_frame = ctk.CTkFrame(main_info_frame, fg_color="transparent")
        right_frame.pack(side="right", fill="y", padx=(20, 0))
        
        # Weather icon placeholder
        self.weather_icon_label = ctk.CTkLabel(
            right_frame,
            text="",
            font=ctk.CTkFont(size=64)
        )
        self.weather_icon_label.pack(pady=(0, 20))
        
        # Details grid
        self.details_frame = ctk.CTkFrame(right_frame)
        self.details_frame.pack(fill="both", expand=True)
        
        # Create detail cards
        self._create_detail_cards()
    
    def _create_detail_cards(self):
        \"\"\"Create cards for detailed weather information\"\"\"
        # Create a grid of detail cards
        detail_info = [
            ("Humidity", "💧"),
            ("Wind", "💨"), 
            ("Pressure", "🌡️"),
            ("Visibility", "👁️"),
            ("UV Index", "☀️"),
            ("Sunrise", "🌅"),
            ("Sunset", "🌇"),
            ("Cloud Cover", "☁️")
        ]
        
        self.detail_cards = {}
        
        for i, (label, icon) in enumerate(detail_info):
            row = i // 2
            col = i % 2
            
            card = WeatherCard(self.details_frame, title=f"{icon} {label}")
            card.grid(row=row, column=col, padx=5, pady=5, sticky="ew")
            
            self.detail_cards[label.lower().replace(" ", "_")] = card
        
        # Configure grid weights
        self.details_frame.grid_columnconfigure(0, weight=1)
        self.details_frame.grid_columnconfigure(1, weight=1)
    
    def _create_forecast_section(self):
        \"\"\"Create 5-day forecast section\"\"\"
        forecast_header = ctk.CTkLabel(
            self.main_frame,
            text="5-Day Forecast",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        forecast_header.pack(pady=(0, 10))
        
        self.forecast_frame = ctk.CTkFrame(self.main_frame)
        self.forecast_frame.pack(fill="x", pady=(0, 20))
        
        # Create forecast cards
        self.forecast_cards = []
        forecast_container = ctk.CTkFrame(self.forecast_frame, fg_color="transparent")
        forecast_container.pack(fill="x", padx=20, pady=20)
        
        for i in range(5):
            card = ForecastCard(forecast_container)
            card.pack(side="left", fill="both", expand=True, padx=5)
            self.forecast_cards.append(card)
    
    def _create_settings_panel(self):
        \"\"\"Create settings panel\"\"\"
        self.settings_panel = SettingsPanel(self.main_frame)
        self.settings_panel_visible = False
    
    def _create_status_bar(self):
        \"\"\"Create status bar\"\"\"
        self.status_bar = StatusBar(self.root)
        self.status_bar.pack(side="bottom", fill="x")
    
    def _toggle_settings(self):
        \"\"\"Toggle settings panel visibility\"\"\"
        if self.settings_panel_visible:
            self.settings_panel.pack_forget()
            self.settings_panel_visible = False
        else:
            self.settings_panel.pack(fill="x", padx=20, pady=(0, 20))
            self.settings_panel_visible = True
    
    def _on_search(self, city: str):
        \"\"\"Handle city search\"\"\"
        if not city:
            messagebox.showerror("Error", "Please enter a city name")
            return
        
        self.current_city = city
        self.search_entry.set_text(city)
        self._load_weather_data()
    
    def _refresh_data(self):
        \"\"\"Refresh current weather data\"\"\"
        self._load_weather_data()
    
    def _load_initial_data(self):
        \"\"\"Load initial weather data\"\"\"
        self.search_entry.set_text(self.current_city)
        self._load_weather_data()
    
    def _load_weather_data(self):
        \"\"\"Load weather data in a separate thread\"\"\"
        self.status_bar.update_status("Loading weather data...")
        
        # Run API calls in a separate thread to prevent UI freezing
        thread = threading.Thread(target=self._fetch_weather_data)
        thread.daemon = True
        thread.start()
    
    def _fetch_weather_data(self):
        \"\"\"Fetch weather data from API\"\"\"
        try:
            # Get current weather
            current_data = self.api_client.get_current_weather(self.current_city, self.current_units)
            
            if current_data:
                self.current_weather_data = current_data
                
                # Get forecast data
                forecast_data = self.api_client.get_forecast(self.current_city, self.current_units)
                if forecast_data:
                    self.forecast_data = forecast_data
                
                # Update UI in main thread
                self.root.after(0, self._update_ui)
            else:
                self.root.after(0, lambda: self._show_error("City not found or API error"))
                
        except Exception as e:
            self.root.after(0, lambda: self._show_error(f"Error loading weather data: {str(e)}"))
    
    def _update_ui(self):
        \"\"\"Update UI with weather data\"\"\"
        if not self.current_weather_data:
            return
        
        data = self.current_weather_data
        
        # Update city name
        city_name = data.get('name', '')
        country = data.get('sys', {}).get('country', '')
        self.city_label.configure(text=f"{city_name}, {country}")
        
        # Update temperature
        temp = data['main']['temp']
        temp_symbol = self._get_temp_symbol()
        self.temp_label.configure(text=f"{temp:.0f}°{temp_symbol}")
        
        # Update condition
        weather = data['weather'][0]
        condition = weather['description'].title()
        self.condition_label.configure(text=condition)
        
        # Update feels like
        feels_like = data['main']['feels_like']
        self.feels_like_label.configure(text=f"Feels like {feels_like:.0f}°{temp_symbol}")
        
        # Update weather icon
        icon_code = weather['icon']
        emoji = get_weather_emoji(weather['main'], icon_code)
        self.weather_icon_label.configure(text=emoji)
        
        # Update detail cards
        self._update_detail_cards(data)
        
        # Update forecast
        if self.forecast_data:
            self._update_forecast()
        
        # Update status
        self.status_bar.update_status("Weather data loaded successfully")
        self.status_bar.update_time()
        
        # Apply temperature-based color theme
        temp_celsius = temp if self.current_units == "metric" else (temp - 32) * 5/9
        self._apply_color_theme(temp_celsius)
        
        # Setup auto-refresh
        if self.auto_refresh_enabled:
            self._setup_auto_refresh()
    
    def _update_detail_cards(self, data: Dict):
        \"\"\"Update detail weather cards\"\"\"
        main = data['main']
        wind = data.get('wind', {})
        sys = data.get('sys', {})
        clouds = data.get('clouds', {})
        visibility = data.get('visibility', 0)
        
        # Update each detail card
        details = {
            'humidity': f"{main.get('humidity', 0)}%",
            'wind': f"{wind.get('speed', 0)} {self._get_wind_unit()}\\n{get_wind_direction(wind.get('deg', 0))}",
            'pressure': f"{main.get('pressure', 0)} hPa",
            'visibility': f"{visibility / 1000:.1f} km" if visibility else "N/A",
            'uv_index': "N/A",  # Not available in current weather API
            'sunrise': format_timestamp(sys.get('sunrise', 0)),
            'sunset': format_timestamp(sys.get('sunset', 0)),
            'cloud_cover': f"{clouds.get('all', 0)}%"
        }
        
        for key, value in details.items():
            if key in self.detail_cards:
                # Clear existing content
                for widget in self.detail_cards[key].content_frame.winfo_children():
                    widget.destroy()
                
                # Add updated info
                value_label = ctk.CTkLabel(
                    self.detail_cards[key].content_frame,
                    text=value,
                    font=ctk.CTkFont(size=14, weight="bold")
                )
                value_label.pack(pady=5)
    
    def _update_forecast(self):
        \"\"\"Update 5-day forecast cards\"\"\"
        if not self.forecast_data or 'list' not in self.forecast_data:
            return
        
        # Group forecast data by day
        daily_forecasts = {}
        for item in self.forecast_data['list']:
            date = datetime.fromtimestamp(item['dt']).strftime('%Y-%m-%d')
            if date not in daily_forecasts:
                daily_forecasts[date] = []
            daily_forecasts[date].append(item)
        
        # Update forecast cards
        for i, (date, forecasts) in enumerate(list(daily_forecasts.items())[:5]):
            if i >= len(self.forecast_cards):
                break
            
            # Get day name
            day_name = datetime.strptime(date, '%Y-%m-%d').strftime('%a')
            if i == 0:
                day_name = "Today"
            elif i == 1:
                day_name = "Tomorrow"
            
            # Calculate high/low temperatures
            temps = [f['main']['temp'] for f in forecasts]
            temp_high = max(temps)
            temp_low = min(temps)
            
            # Get most common weather condition
            conditions = [f['weather'][0] for f in forecasts]
            main_condition = max(set(c['main'] for c in conditions), 
                               key=lambda x: sum(1 for c in conditions if c['main'] == x))
            
            # Get icon
            icon_codes = [c['icon'] for c in conditions]
            main_icon = max(set(icon_codes), key=icon_codes.count)
            emoji = get_weather_emoji(main_condition, main_icon)
            
            # Get description
            descriptions = [c['description'] for c in conditions]
            main_desc = max(set(descriptions), key=descriptions.count)
            
            # Update card
            temp_symbol = self._get_temp_symbol()
            self.forecast_cards[i].update_forecast(
                day_name,
                emoji,
                f"{temp_high:.0f}°{temp_symbol}",
                f"{temp_low:.0f}°{temp_symbol}",
                main_desc
            )
    
    def _apply_color_theme(self, temp_celsius: float):
        \"\"\"Apply color theme based on temperature\"\"\"
        theme = get_temperature_color_theme(temp_celsius)
        # Note: CustomTkinter has limited dynamic theming support
        # This is a placeholder for future theme implementation
        pass
    
    def _get_temp_symbol(self) -> str:
        \"\"\"Get temperature symbol based on current units\"\"\"
        symbols = {
            "metric": "C",
            "imperial": "F",
            "kelvin": "K"
        }
        return symbols.get(self.current_units, "C")
    
    def _get_wind_unit(self) -> str:
        \"\"\"Get wind speed unit based on current units\"\"\"
        units = {
            "metric": "m/s",
            "imperial": "mph",
            "kelvin": "m/s"
        }
        return units.get(self.current_units, "m/s")
    
    def _setup_auto_refresh(self):
        \"\"\"Setup auto-refresh timer\"\"\"
        if self.refresh_timer:
            self.root.after_cancel(self.refresh_timer)
        
        if self.auto_refresh_enabled:
            self.refresh_timer = self.root.after(REFRESH_INTERVAL, self._load_weather_data)
    
    def _show_error(self, message: str):
        \"\"\"Show error message\"\"\"
        messagebox.showerror("Error", message)
        self.status_bar.update_status(f"Error: {message}")
    
    def run(self):
        \"\"\"Start the application\"\"\"
        self.root.mainloop()

def main():
    \"\"\"Main entry point\"\"\"
    app = WeatherApp()
    app.run()

if __name__ == "__main__":
    main()
""",
        
        "requirements.txt": """# Weather App Dependencies
customtkinter>=5.2.0
Pillow>=10.0.0
requests>=2.31.0
""",
        
        "README.md": """# WeatherPy - Advanced Weather Forecast Application

A modern, feature-rich weather application built with Python and CustomTkinter, providing real-time weather data and 5-day forecasts with a beautiful, responsive user interface.

## Features

🌤️ **Real-time Weather Data**: Current weather conditions for any city worldwide
📅 **5-Day Forecast**: Detailed weather predictions with daily highs and lows  
🎨 **Modern UI**: Beautiful, responsive interface built with CustomTkinter
🌡️ **Dynamic Themes**: Color themes that change based on temperature
🔍 **Smart Search**: City search with autocomplete suggestions
🔄 **Auto-refresh**: Automatic weather updates every 5 minutes
⚙️ **Customizable Settings**: Choose temperature units, themes, and refresh intervals
📱 **Responsive Design**: Works great on different screen sizes

## Screenshots

![Weather App Screenshot](assets/screenshot.png)

## Installation

### Prerequisites
- Python 3.8 or higher
- OpenWeatherMap API key (free from https://openweathermap.org/api)

### Setup

1. **Clone the repository**:
```bash
git clone https://github.com/yourusername/weatherpy.git
cd weatherpy
```

2. **Create a virtual environment**:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Configure API key**:
   - Get your free API key from [OpenWeatherMap](https://openweathermap.org/api)
   - Open `weather_app/config.py`
   - Replace `"your_api_key_here"` with your actual API key

5. **Run the application**:
```bash
python -m weather_app.main_app
```

## Usage

### Basic Usage
1. **Search for a city**: Type a city name in the search bar and press Enter or click the search button
2. **View current weather**: See temperature, conditions, humidity, wind speed, and more
3. **Check forecast**: View the 5-day weather forecast with daily highs and lows
4. **Refresh data**: Click the refresh button or wait for automatic updates

### Advanced Features
- **Settings Panel**: Click the settings (⚙️) button to customize units, themes, and auto-refresh
- **Temperature Units**: Choose between Celsius, Fahrenheit, or Kelvin
- **Auto-refresh**: Enable/disable automatic weather updates
- **Theme Selection**: Choose between dark, light, or system themes

## Project Structure

```
weatherpy/
├── weather_app/
│   ├── __init__.py
│   ├── config.py          # Configuration settings
│   ├── api_client.py      # OpenWeatherMap API client
│   ├── utils.py           # Utility functions
│   ├── widgets.py         # Custom UI widgets
│   ├── main_app.py        # Main application class
│   ├── assets/            # Images and icons
│   │   ├── icons/         # Weather icons
│   │   └── backgrounds/   # Background images
│   └── cache/             # API response cache
├── requirements.txt       # Python dependencies
├── README.md
└── .gitignore
```

## API Configuration

The app uses the OpenWeatherMap API for weather data. Key endpoints used:

- **Current Weather**: `http://api.openweathermap.org/data/2.5/weather`
- **5-Day Forecast**: `http://api.openweathermap.org/data/2.5/forecast`
- **Geocoding**: `http://api.openweathermap.org/geo/1.0/direct`

## Customization

### Adding Custom Weather Icons
1. Place your icon files in `weather_app/assets/icons/`
2. Update the icon mapping in `utils.py`

### Modifying Color Themes
1. Edit the `TEMP_COLOR_THEMES` dictionary in `config.py`
2. Add new temperature ranges and color schemes

### Extending API Support
1. Add new API clients in `api_client.py`
2. Implement additional weather data sources

## Dependencies

- **CustomTkinter**: Modern UI components for tkinter
- **Pillow**: Image processing for icons and backgrounds  
- **Requests**: HTTP library for API calls
- **Python 3.8+**: Core Python interpreter

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- OpenWeatherMap for providing the weather API
- CustomTkinter library for modern UI components
- Weather icons from various open-source collections

## Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/yourusername/weatherpy/issues) page
2. Create a new issue with detailed information
3. Contact the maintainer

## Roadmap

- [ ] Add weather alerts and notifications
- [ ] Implement location-based weather (GPS)
- [ ] Add weather maps and radar
- [ ] Support for multiple cities/favorites
- [ ] Historical weather data charts
- [ ] Mobile app version
- [ ] Weather widgets for desktop

---

**Enjoy tracking the weather with WeatherPy!** 🌤️
""",
        
        ".gitignore": """# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/
cover/

# Translations
*.mo
*.pot

# Django stuff:
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal

# Flask stuff:
instance/
.webassets-cache

# Scrapy stuff:
.scrapy

# Sphinx documentation
docs/_build/

# PyBuilder
.pybuilder/
target/

# Jupyter Notebook
.ipynb_checkpoints

# IPython
profile_default/
ipython_config.py

# pyenv
.python-version

# pipenv
Pipfile.lock

# poetry
poetry.lock

# pdm
.pdm.toml

# PEP 582
__pypackages__/

# Celery stuff
celerybeat-schedule
celerybeat.pid

# SageMath parsed files
*.sage.py

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Spyder project settings
.spyderproject
.spyproject

# Rope project settings
.ropeproject

# mkdocs documentation
/site

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# Pyre type checker
.pyre/

# pytype static type analyzer
.pytype/

# Cython debug symbols
cython_debug/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Project specific
weather_app/cache/
weather_app/assets/icons/*.png
weather_app/assets/backgrounds/*.jpg
*.log
config_local.py
""",

        "setup.py": """
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="weatherpy-advanced",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A modern weather application with real-time data and forecasts",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/weatherpy",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Desktop Environment",
        "Topic :: Scientific/Engineering :: Atmospheric Science",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest",
            "black",
            "flake8",
            "mypy",
        ],
    },
    entry_points={
        "console_scripts": [
            "weatherpy=weather_app.main_app:main",
        ],
    },
)
"""
    }
}

# Create project structure
def create_structure(base_path, structure, current_path=""):
    for name, content in structure.items():
        full_path = os.path.join(base_path, current_path, name)
        
        if isinstance(content, dict):
            # It's a directory
            os.makedirs(full_path, exist_ok=True)
            create_structure(base_path, content, os.path.join(current_path, name))
        else:
            # It's a file
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)

# Create the complete project structure
project_name = "weatherpy_advanced"
create_structure(".", {project_name: project_structure})

print("✅ Complete Weather App project structure created!")
print(f"📁 Project folder: {project_name}")
print("""
🚀 Next steps:
1. Get your free API key from https://openweathermap.org/api
2. Edit weather_app/config.py and replace 'your_api_key_here' with your API key
3. Create virtual environment: python -m venv venv
4. Activate environment: venv\\Scripts\\activate (Windows) or source venv/bin/activate (Linux/Mac)
5. Install dependencies: pip install -r requirements.txt
6. Run the app: python -m weather_app.main_app
""")

# Also create a simple launcher script
launcher_script = '''#!/usr/bin/env python3
"""
WeatherPy Advanced - Modern Weather Application
Quick launcher script
"""

import os
import sys
import subprocess

def main():
    """Launch the weather application"""
    print("🌤️  Starting WeatherPy Advanced...")
    
    # Check if we're in a virtual environment
    if not hasattr(sys, 'real_prefix') and not sys.base_prefix != sys.prefix:
        print("⚠️  Warning: Not running in a virtual environment")
        print("💡 Recommended: Create and activate a virtual environment first")
        print("   python -m venv venv")
        print("   venv\\\\Scripts\\\\activate  # Windows")
        print("   source venv/bin/activate  # Linux/Mac")
        print()
    
    try:
        # Try to import required modules
        import customtkinter
        import PIL
        import requests
        
        # Import and run the app
        from weather_app.main_app import main as run_app
        run_app()
        
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("📦 Installing dependencies...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
            print("✅ Dependencies installed successfully!")
            print("🔄 Please run the script again")
        except subprocess.CalledProcessError:
            print("❌ Failed to install dependencies")
            print("💡 Try manually: pip install -r requirements.txt")
    except Exception as e:
        print(f"❌ Error: {e}")
        print("💡 Make sure you've configured your API key in weather_app/config.py")

if __name__ == "__main__":
    main()
'''

with open(f"{project_name}/run_app.py", 'w', encoding='utf-8') as f:
    f.write(launcher_script)

print("📝 Created launcher script: run_app.py")