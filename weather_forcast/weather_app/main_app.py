import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
from datetime import datetime, timedelta
import threading
from typing import Optional, Dict
import os
from PIL import Image, ImageTk, ImageFilter, ImageEnhance
from .api_client import WeatherAPIClient
from .widgets import ModernSearchEntry, WeatherCard, ForecastCard, SettingsPanel, StatusBar
from .utils import get_temperature_color_theme, get_weather_emoji, get_wind_direction, format_timestamp
from .config import (
    APP_NAME, WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT,
    DEFAULT_CITY, DEFAULT_UNITS, REFRESH_INTERVAL
)

class WeatherApp:
    """Main Weather Application Class with Glass Effect UI"""

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

        # Background image handling
        self.background_label = None
        self.current_background = None
        self.background_images = {}
        self.blurred_background = None
        
        # Glass effect color scheme (CustomTkinter compatible - NO TRANSPARENCY TUPLES)
        self.glass_colors = {
            # Using semi-transparent single colors instead of tuples
            "main_bg": "#1a1a1a",           # Dark background
            "glass_light": "#2d2d2d",       # Light glass effect
            "glass_medium": "#242424",       # Medium glass effect
            "glass_dark": "#1f1f1f",        # Dark glass effect
            "glass_darker": "#1a1a1a",      # Darker glass effect
            "accent": "#3d8bff",            # Blue accent
            "accent_hover": "#4a94ff",      # Blue accent hover
            "text_white": "#ffffff",        # White text
            "text_light": "#e0e0e0",        # Light text
            "text_medium": "#b0b0b0",       # Medium text
            "text_dark": "#808080",         # Dark text
            "border_light": "#404040",      # Light border
            "success": "#28a745",           # Success green
            "warning": "#ffc107",           # Warning yellow
            "error": "#dc3545"              # Error red
        }
        
        # Load background images
        self._load_background_images()

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

    def _load_background_images(self):
        """Load background images from assets/backgrounds/ directory"""
        # Try multiple possible paths for the backgrounds directory
        possible_paths = [
            "assets/backgrounds",
            "./assets/backgrounds", 
            "backgrounds",
            "./backgrounds",
            os.path.join(os.path.dirname(__file__), "assets", "backgrounds"),
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "backgrounds")
        ]
        
        backgrounds_dir = None
        for path in possible_paths:
            if os.path.exists(path):
                backgrounds_dir = path
                print(f"Found backgrounds directory: {backgrounds_dir}")
                break
        
        if not backgrounds_dir:
            print("No backgrounds directory found. Creating default background.")
            self._create_default_background()
            return
        
        # Look for any image files in the directory
        supported_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif']
        found_files = []
        
        try:
            for file in os.listdir(backgrounds_dir):
                if any(file.lower().endswith(ext) for ext in supported_extensions):
                    found_files.append(file)
        except Exception as e:
            print(f"Error reading backgrounds directory: {e}")
            self._create_default_background()
            return
        
        print(f"Found {len(found_files)} image files: {found_files}")
        
        # Default background mappings for different weather conditions
        background_mappings = {
            'clear_day': ['sunny', 'clear_day', 'sunshine', 'clear', 'day'],
            'clear_night': ['clear_night', 'starry_night', 'night_clear', 'night', 'stars'],
            'clouds': ['cloudy', 'overcast', 'clouds', 'cloud'],
            'rain': ['rainy', 'rain', 'storm', 'raining'],
            'snow': ['snowy', 'snow', 'winter', 'snowing'],
            'thunderstorm': ['thunderstorm', 'storm', 'lightning', 'thunder'],
            'drizzle': ['drizzle', 'light_rain', 'misty', 'mist'],
            'mist': ['misty', 'fog', 'hazy', 'mist'],
            'fog': ['fog', 'misty', 'hazy', 'foggy'],
            'default': ['default', 'sky', 'landscape', 'background']
        }
        
        self.background_mappings = background_mappings
        
        # Match found files to categories
        for category, keywords in background_mappings.items():
            for keyword in keywords:
                matching_files = [f for f in found_files if keyword.lower() in f.lower()]
                if matching_files:
                    filepath = os.path.join(backgrounds_dir, matching_files[0])
                    try:
                        test_image = Image.open(filepath)
                        test_image.close()
                        self.background_images[category] = filepath
                        print(f"Mapped '{category}' to '{matching_files[0]}'")
                        break
                    except Exception as e:
                        print(f"Error testing image {filepath}: {e}")
                        continue
        
        # If no specific mappings found, use any available images as defaults
        if len(self.background_images) == 0 and found_files:
            print("No specific mappings found, using first available image as default")
            filepath = os.path.join(backgrounds_dir, found_files[0])
            try:
                test_image = Image.open(filepath)
                test_image.close()
                self.background_images['default'] = filepath
                for category in ['clear_day', 'clouds', 'rain', 'snow']:
                    self.background_images[category] = filepath
            except Exception as e:
                print(f"Error with fallback image {filepath}: {e}")
                self._create_default_background()
                return
        
        if len(self.background_images) == 0:
            self._create_default_background()
        else:
            print(f"Successfully loaded {len(self.background_images)} background images")

    def _create_default_background(self):
        """Create a default gradient background if no images are found"""
        width, height = WINDOW_WIDTH, WINDOW_HEIGHT
        image = Image.new('RGB', (width, height), color=(74, 144, 226))
        
        # Create gradient effect
        for y in range(height):
            r = int(74 + (144 - 74) * y / height)
            g = int(144 + (102 - 144) * y / height)  
            b = int(226 + (185 - 226) * y / height)
            
            for x in range(width):
                image.putpixel((x, y), (r, g, b))
        
        # Save to temp file
        import tempfile
        temp_path = os.path.join(tempfile.gettempdir(), 'default_weather_bg.png')
        image.save(temp_path)
        
        self.background_images['default'] = temp_path
        for category in ['clear_day', 'clouds', 'rain', 'snow', 'clear_night']:
            self.background_images[category] = temp_path

    def _get_appropriate_background(self, weather_data: Dict) -> str:
        """Determine the most appropriate background based on weather conditions"""
        if not weather_data:
            return self.background_images.get('default')
        
        try:
            weather = weather_data['weather'][0]
            main_condition = weather['main'].lower()
            icon_code = weather['icon']
            temp = weather_data['main']['temp']
            
            # Check if it's day or night from icon code
            is_day = icon_code.endswith('d')
            
            # Weather condition mappings
            weather_backgrounds = {
                'thunderstorm': 'thunderstorm',
                'drizzle': 'drizzle',
                'rain': 'rain',
                'snow': 'snow',
                'mist': 'mist',
                'smoke': 'mist',
                'haze': 'mist',
                'dust': 'mist',
                'fog': 'fog',
                'sand': 'mist',
                'ash': 'mist',
                'squall': 'thunderstorm',
                'tornado': 'thunderstorm',
                'clear': 'clear_day' if is_day else 'clear_night',
                'clouds': 'clouds'
            }
            
            if main_condition in weather_backgrounds:
                bg_key = weather_backgrounds[main_condition]
                if bg_key in self.background_images:
                    return self.background_images[bg_key]
        
        except Exception as e:
            print(f"Error determining background: {e}")
        
        return self.background_images.get('default')

    def _create_glass_background(self, image_path: str) -> ImageTk.PhotoImage:
        """Create a background with glass effect (high blur, darkened)"""
        if not image_path or not os.path.exists(image_path):
            return None
        
        try:
            image = Image.open(image_path)
            
            # Get current window size
            self.root.update_idletasks()
            window_width = self.root.winfo_width()
            window_height = self.root.winfo_height()
            
            if window_width < 100 or window_height < 100:
                window_width = WINDOW_WIDTH
                window_height = WINDOW_HEIGHT
            
            # Resize and crop image to fit window
            image_ratio = image.width / image.height
            window_ratio = window_width / window_height
            
            if image_ratio > window_ratio:
                new_height = window_height
                new_width = int(window_height * image_ratio)
            else:
                new_width = window_width
                new_height = int(window_width / image_ratio)
            
            image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Center crop
            if new_width > window_width:
                left = (new_width - window_width) // 2
                image = image.crop((left, 0, left + window_width, new_height))
            elif new_height > window_height:
                top = (new_height - window_height) // 2
                image = image.crop((0, top, new_width, top + window_height))
            
            # Apply heavy blur for glass effect
            blurred = image.filter(ImageFilter.GaussianBlur(radius=25))
            
            # Darken the image significantly for better contrast
            enhancer = ImageEnhance.Brightness(blurred)
            darkened = enhancer.enhance(0.4)  # Make it 40% of original brightness
            
            return ImageTk.PhotoImage(darkened)
            
        except Exception as e:
            print(f"Error creating glass background: {e}")
            return None

    def _update_background(self, image_path: str):
        """Update the background image"""
        if not image_path or not os.path.exists(image_path):
            return
        
        try:
            glass_bg = self._create_glass_background(image_path)
            if not glass_bg:
                return
            
            if self.background_label is None:
                self.background_label = tk.Label(self.root, image=glass_bg, bg=self.glass_colors["main_bg"])
                self.background_label.place(x=0, y=0, relwidth=1, relheight=1)
            else:
                self.background_label.configure(image=glass_bg)
                self.background_label.place(x=0, y=0, relwidth=1, relheight=1)
            
            self.blurred_background = glass_bg
            self.background_label.lower()
            
            # Ensure UI elements are above background
            if self.main_frame:
                self.main_frame.lift()
                
        except Exception as e:
            print(f"Error updating background: {e}")

    def _setup_ui(self):
        """Setup the user interface with proper glass effect"""
        # Set root background
        self.root.configure(bg=self.glass_colors["main_bg"])
        
        # Create main frame with glass effect (no transparency tuple)
        self.main_frame = ctk.CTkFrame(
            self.root, 
            fg_color=self.glass_colors["glass_light"],
            corner_radius=20,
            border_width=1,
            border_color=self.glass_colors["border_light"]
        )
        self.main_frame.pack(fill="both", expand=True, padx=30, pady=30)
        
        self._create_top_section()
        self._create_current_weather_section()
        self._create_forecast_section()
        self._create_settings_panel()
        self._create_status_bar()
        
        self.root.bind('<Configure>', self._on_window_resize)

    def _on_window_resize(self, event):
        """Handle window resize event"""
        if event.widget == self.root and hasattr(self, 'current_weather_data') and self.current_weather_data:
            if hasattr(self, '_resize_timer'):
                self.root.after_cancel(self._resize_timer)
            self._resize_timer = self.root.after(500, self._delayed_background_update)

    def _delayed_background_update(self):
        """Update background after delay"""
        if self.current_weather_data:
            background_path = self._get_appropriate_background(self.current_weather_data)
            if background_path:
                self._update_background(background_path)

    def _create_top_section(self):
        """Create top section with search and controls"""
        top_frame = ctk.CTkFrame(
            self.main_frame, 
            fg_color=self.glass_colors["glass_medium"],
            corner_radius=15,
            border_width=1,
            border_color=self.glass_colors["border_light"]
        )
        top_frame.pack(fill="x", pady=(0, 20))

        # Search section
        search_frame = ctk.CTkFrame(
            top_frame, 
            fg_color=self.glass_colors["glass_dark"],
            corner_radius=12
        )
        search_frame.pack(side="left", fill="x", expand=True, padx=(20, 10), pady=20)

        self.search_entry = ModernSearchEntry(
            search_frame,
            search_callback=self._on_search
        )
        self.search_entry.pack(fill="x", padx=15, pady=15)

        # Controls section
        controls_frame = ctk.CTkFrame(
            top_frame, 
            fg_color=self.glass_colors["glass_dark"],
            corner_radius=12
        )
        controls_frame.pack(side="right", padx=(10, 20), pady=20)

        # Refresh button
        self.refresh_button = ctk.CTkButton(
            controls_frame,
            text="🔄",
            command=self._refresh_data,
            width=50,
            height=40,
            font=ctk.CTkFont(size=18),
            fg_color=self.glass_colors["accent"],
            hover_color=self.glass_colors["accent_hover"]
        )
        self.refresh_button.pack(side="left", padx=(15, 5), pady=15)

        # Settings button
        self.settings_button = ctk.CTkButton(
            controls_frame,
            text="⚙️",
            command=self._toggle_settings,
            width=50,
            height=40,
            font=ctk.CTkFont(size=18),
            fg_color=self.glass_colors["accent"],
            hover_color=self.glass_colors["accent_hover"]
        )
        self.settings_button.pack(side="left", padx=(5, 15), pady=15)

    def _create_current_weather_section(self):
        """Create current weather display section"""
        self.current_weather_frame = ctk.CTkFrame(
            self.main_frame, 
            fg_color=self.glass_colors["glass_medium"],
            corner_radius=15,
            border_width=1,
            border_color=self.glass_colors["border_light"]
        )
        self.current_weather_frame.pack(fill="x", pady=(0, 20))

        # Main weather container
        main_container = ctk.CTkFrame(
            self.current_weather_frame,
            fg_color=self.glass_colors["glass_dark"],
            corner_radius=12
        )
        main_container.pack(fill="x", padx=20, pady=20)

        # Left side - Temperature and location
        left_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        left_frame.pack(side="left", fill="both", expand=True, padx=20, pady=20)

        self.city_label = ctk.CTkLabel(
            left_frame,
            text="Loading...",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=self.glass_colors["text_white"]
        )
        self.city_label.pack(anchor="w", pady=(0, 5))

        self.temp_label = ctk.CTkLabel(
            left_frame,
            text="--°",
            font=ctk.CTkFont(size=64, weight="bold"),
            text_color=self.glass_colors["text_white"]
        )
        self.temp_label.pack(anchor="w", pady=(0, 5))

        self.condition_label = ctk.CTkLabel(
            left_frame,
            text="--",
            font=ctk.CTkFont(size=18),
            text_color=self.glass_colors["text_light"]
        )
        self.condition_label.pack(anchor="w", pady=(0, 5))

        self.feels_like_label = ctk.CTkLabel(
            left_frame,
            text="--",
            font=ctk.CTkFont(size=14),
            text_color=self.glass_colors["text_medium"]
        )
        self.feels_like_label.pack(anchor="w")

        # Right side - Icon and details
        right_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        right_frame.pack(side="right", fill="y", padx=(0, 20), pady=20)

        self.weather_icon_label = ctk.CTkLabel(
            right_frame,
            text="🌤️",
            font=ctk.CTkFont(size=48)
        )
        self.weather_icon_label.pack(pady=(0, 15))

        # Details container
        self.details_container = ctk.CTkFrame(
            right_frame,
            fg_color=self.glass_colors["glass_darker"],
            corner_radius=10
        )
        self.details_container.pack(fill="both", expand=True)

        self._create_detail_cards()

    def _create_detail_cards(self):
        """Create detail weather cards"""
        details_info = [
            ("Humidity", "💧", "humidity"),
            ("Wind", "💨", "wind"),
            ("Pressure", "🌡️", "pressure"),
            ("Visibility", "👁️", "visibility")
        ]

        self.detail_labels = {}

        for i, (name, icon, key) in enumerate(details_info):
            row = i // 2
            col = i % 2

            # Card container
            card = ctk.CTkFrame(
                self.details_container,
                fg_color=self.glass_colors["glass_light"],
                corner_radius=8
            )
            card.grid(row=row, column=col, padx=5, pady=5, sticky="ew")

            # Card content
            title_label = ctk.CTkLabel(
                card,
                text=f"{icon} {name}",
                font=ctk.CTkFont(size=10, weight="bold"),
                text_color=self.glass_colors["text_medium"]
            )
            title_label.pack(pady=(8, 2))

            value_label = ctk.CTkLabel(
                card,
                text="--",
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color=self.glass_colors["text_white"]
            )
            value_label.pack(pady=(0, 8))

            self.detail_labels[key] = value_label

        # Configure grid
        self.details_container.grid_columnconfigure(0, weight=1)
        self.details_container.grid_columnconfigure(1, weight=1)

    def _create_forecast_section(self):
        """Create 5-day forecast section"""
        forecast_title = ctk.CTkLabel(
            self.main_frame,
            text="5-Day Forecast",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=self.glass_colors["text_white"]
        )
        forecast_title.pack(pady=(0, 10))

        self.forecast_frame = ctk.CTkFrame(
            self.main_frame, 
            fg_color=self.glass_colors["glass_medium"],
            corner_radius=15,
            border_width=1,
            border_color=self.glass_colors["border_light"]
        )
        self.forecast_frame.pack(fill="x", pady=(0, 20))

        # Forecast container
        forecast_container = ctk.CTkFrame(
            self.forecast_frame,
            fg_color="transparent"
        )
        forecast_container.pack(fill="x", padx=20, pady=20)

        self.forecast_cards = []
        for i in range(5):
            card = self._create_forecast_card(forecast_container)
            card.pack(side="left", fill="both", expand=True, padx=2)
            self.forecast_cards.append(card)

    def _create_forecast_card(self, parent):
        """Create individual forecast card"""
        card = ctk.CTkFrame(
            parent,
            fg_color=self.glass_colors["glass_dark"],
            corner_radius=12
        )

        # Create card structure
        card.day_label = ctk.CTkLabel(
            card,
            text="",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=self.glass_colors["text_white"]
        )
        card.day_label.pack(pady=(15, 5))

        card.icon_label = ctk.CTkLabel(
            card,
            text="",
            font=ctk.CTkFont(size=28)
        )
        card.icon_label.pack(pady=5)

        card.high_label = ctk.CTkLabel(
            card,
            text="",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=self.glass_colors["text_white"]
        )
        card.high_label.pack()

        card.low_label = ctk.CTkLabel(
            card,
            text="",
            font=ctk.CTkFont(size=14),
            text_color=self.glass_colors["text_medium"]
        )
        card.low_label.pack()

        card.desc_label = ctk.CTkLabel(
            card,
            text="",
            font=ctk.CTkFont(size=10),
            text_color=self.glass_colors["text_medium"],
            wraplength=80
        )
        card.desc_label.pack(pady=(5, 15))

        # Add update method
        def update_forecast(day, icon, high, low, desc):
            card.day_label.configure(text=day)
            card.icon_label.configure(text=icon)
            card.high_label.configure(text=high)
            card.low_label.configure(text=low)
            card.desc_label.configure(text=desc)

        card.update_forecast = update_forecast
        return card

    def _create_settings_panel(self):
        """Create settings panel"""
        self.settings_panel = ctk.CTkFrame(
            self.main_frame,
            fg_color=self.glass_colors["glass_medium"],
            corner_radius=15
        )
        self.settings_panel_visible = False

        # Settings title
        settings_title = ctk.CTkLabel(
            self.settings_panel,
            text="Settings",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=self.glass_colors["text_white"]
        )
        settings_title.pack(pady=(20, 10))

        # Units setting
        units_frame = ctk.CTkFrame(self.settings_panel, fg_color="transparent")
        units_frame.pack(fill="x", padx=20, pady=10)

        units_label = ctk.CTkLabel(
            units_frame,
            text="Temperature Units:",
            font=ctk.CTkFont(size=14),
            text_color=self.glass_colors["text_light"]
        )
        units_label.pack(side="left")

        self.units_var = tk.StringVar(value=self.current_units)
        self.units_menu = ctk.CTkOptionMenu(
            units_frame,
            values=["metric", "imperial", "kelvin"],
            variable=self.units_var,
            command=self._on_units_change,
            fg_color=self.glass_colors["accent"],
            button_color=self.glass_colors["accent_hover"],
            dropdown_fg_color=self.glass_colors["glass_dark"]
        )
        self.units_menu.pack(side="right")

        # Auto-refresh setting
        refresh_frame = ctk.CTkFrame(self.settings_panel, fg_color="transparent")
        refresh_frame.pack(fill="x", padx=20, pady=(10, 20))

        refresh_label = ctk.CTkLabel(
            refresh_frame,
            text="Auto Refresh:",
            font=ctk.CTkFont(size=14),
            text_color=self.glass_colors["text_light"]
        )
        refresh_label.pack(side="left")

        self.auto_refresh_var = tk.BooleanVar(value=self.auto_refresh_enabled)
        self.refresh_switch = ctk.CTkSwitch(
            refresh_frame,
            variable=self.auto_refresh_var,
            command=self._on_auto_refresh_change,
            fg_color=self.glass_colors["glass_dark"],
            progress_color=self.glass_colors["accent"]
        )
        self.refresh_switch.pack(side="right")

    def _create_status_bar(self):
        """Create status bar"""
        self.status_bar = ctk.CTkFrame(
            self.root,
            fg_color=self.glass_colors["glass_darker"],
            corner_radius=0,
            height=30
        )
        
        self.status_label = ctk.CTkLabel(
            self.status_bar,
            text="Ready",
            font=ctk.CTkFont(size=11),
            text_color=self.glass_colors["text_medium"]
        )
        self.status_label.pack(side="left", padx=15, pady=5)
        
        self.time_label = ctk.CTkLabel(
            self.status_bar,
            text="",
            font=ctk.CTkFont(size=11),
            text_color=self.glass_colors["text_medium"]
        )
        self.time_label.pack(side="right", padx=15, pady=5)
        
        self.status_bar.pack(side="bottom", fill="x")

        # Add methods to status bar
        def update_status(message):
            self.status_label.configure(text=message)
        
        def update_time():
            current_time = datetime.now().strftime("%I:%M %p")
            self.time_label.configure(text=current_time)
        
        self.status_bar.update_status = update_status
        self.status_bar.update_time = update_time

    def _toggle_settings(self):
        """Toggle settings panel visibility"""
        if self.settings_panel_visible:
            self.settings_panel.pack_forget()
            self.settings_panel_visible = False
        else:
            self.settings_panel.pack(fill="x", padx=30, pady=(0, 20))
            self.settings_panel_visible = True

    def _on_units_change(self, units: str):
        """Handle units change"""
        self.current_units = units
        self._load_weather_data()

    def _on_auto_refresh_change(self):
        """Handle auto-refresh toggle"""
        self.auto_refresh_enabled = self.auto_refresh_var.get()
        if self.auto_refresh_enabled:
            self._setup_auto_refresh()
        else:
            if self.refresh_timer:
                self.root.after_cancel(self.refresh_timer)
                self.refresh_timer = None

    def _on_search(self, city: str):
        """Handle city search"""
        if not city:
            messagebox.showerror("Error", "Please enter a city name")
            return
        self.current_city = city
        self._load_weather_data()

    def _refresh_data(self):
        """Refresh weather data"""
        self._load_weather_data()

    def _load_initial_data(self):
        """Load initial weather data"""
        self._load_weather_data()

    def _load_weather_data(self):
        """Load weather data in a separate thread"""
        self.status_bar.update_status("Loading weather data...")
        
        thread = threading.Thread(target=self._fetch_weather_data)
        thread.daemon = True
        thread.start()

    def _fetch_weather_data(self):
        """Fetch weather data from API"""
        try:
            current_data = self.api_client.get_current_weather(self.current_city, self.current_units)

            if current_data:
                self.current_weather_data = current_data
                forecast_data = self.api_client.get_forecast(self.current_city, self.current_units)
                if forecast_data:
                    self.forecast_data = forecast_data

                self.root.after(0, self._update_ui)
            else:
                self.root.after(0, lambda: self._show_error("City not found or API error"))

        except Exception as e:
            self.root.after(0, lambda: self._show_error(f"Error loading weather data: {str(e)}"))

    def _update_ui(self):
        """Update UI with weather data"""
        if not self.current_weather_data:
            return

        data = self.current_weather_data

        # Update background
        background_path = self._get_appropriate_background(data)
        if background_path:
            self._update_background(background_path)

        # Update main weather info
        city_name = data.get('name', '')
        country = data.get('sys', {}).get('country', '')
        self.city_label.configure(text=f"{city_name}, {country}")

        temp = data['main']['temp']
        temp_symbol = self._get_temp_symbol()
        self.temp_label.configure(text=f"{temp:.0f}°{temp_symbol}")

        weather = data['weather'][0]
        condition = weather['description'].title()
        self.condition_label.configure(text=condition)

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

        # Setup auto-refresh
        if self.auto_refresh_enabled:
            self._setup_auto_refresh()

    def _update_detail_cards(self, data: Dict):
        """Update detail weather cards"""
        main = data['main']
        wind = data.get('wind', {})
        visibility = data.get('visibility', 0)

        # Update detail values
        if 'humidity' in self.detail_labels:
            self.detail_labels['humidity'].configure(text=f"{main.get('humidity', 0)}%")

        if 'wind' in self.detail_labels:
            wind_speed = wind.get('speed', 0)
            wind_unit = self._get_wind_unit()
            wind_dir = get_wind_direction(wind.get('deg', 0))
            self.detail_labels['wind'].configure(text=f"{wind_speed} {wind_unit}\n{wind_dir}")

        if 'pressure' in self.detail_labels:
            self.detail_labels['pressure'].configure(text=f"{main.get('pressure', 0)} hPa")

        if 'visibility' in self.detail_labels:
            vis_text = f"{visibility / 1000:.1f} km" if visibility else "N/A"
            self.detail_labels['visibility'].configure(text=vis_text)

    def _update_forecast(self):
        """Update 5-day forecast cards"""
        if not self.forecast_data or 'list' not in self.forecast_data:
            return

        # Group forecast by day
        daily_forecasts = {}
        for item in self.forecast_data['list']:
            date = datetime.fromtimestamp(item['dt']).strftime('%Y-%m-%d')
            if date not in daily_forecasts:
                daily_forecasts[date] = []
            daily_forecasts[date].append(item)

        # Update forecast cards
        temp_symbol = self._get_temp_symbol()
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

            # Get icon and description
            icon_codes = [c['icon'] for c in conditions]
            main_icon = max(set(icon_codes), key=icon_codes.count)
            emoji = get_weather_emoji(main_condition, main_icon)

            descriptions = [c['description'] for c in conditions]
            main_desc = max(set(descriptions), key=descriptions.count)

            # Update card
            self.forecast_cards[i].update_forecast(
                day_name,
                emoji,
                f"{temp_high:.0f}°{temp_symbol}",
                f"{temp_low:.0f}°{temp_symbol}",
                main_desc.title()
            )

    def _get_temp_symbol(self) -> str:
        """Get temperature symbol based on current units"""
        symbols = {
            "metric": "C",
            "imperial": "F", 
            "kelvin": "K"
        }
        return symbols.get(self.current_units, "C")

    def _get_wind_unit(self) -> str:
        """Get wind speed unit based on current units"""
        units = {
            "metric": "m/s",
            "imperial": "mph",
            "kelvin": "m/s"
        }
        return units.get(self.current_units, "m/s")

    def _setup_auto_refresh(self):
        """Setup auto-refresh timer"""
        if self.refresh_timer:
            self.root.after_cancel(self.refresh_timer)

        if self.auto_refresh_enabled:
            self.refresh_timer = self.root.after(REFRESH_INTERVAL, self._load_weather_data)

    def _show_error(self, message: str):
        """Show error message"""
        messagebox.showerror("Error", message)
        self.status_bar.update_status(f"Error: {message}")

    def run(self):
        """Start the application"""
        self.root.mainloop()

def main():
    """Main entry point"""
    app = WeatherApp()
    app.run()

if __name__ == "__main__":
    main()