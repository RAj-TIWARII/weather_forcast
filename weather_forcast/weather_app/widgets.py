
import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from typing import Callable, Optional, List, Dict
from datetime import datetime

class ModernSearchEntry(ctk.CTkFrame):
    """Modern search entry with autocomplete functionality"""

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
        """Handle search text changes for autocomplete"""
        query = self.search_var.get().strip()
        if len(query) >= 2:
            # Here you would typically call an API to get city suggestions
            # For now, we'll just hide the dropdown
            self._hide_dropdown()

    def _on_search_click(self):
        """Handle search button click"""
        if self.search_callback:
            self.search_callback(self.search_var.get().strip())
        self._hide_dropdown()

    def _hide_dropdown(self, event=None):
        """Hide autocomplete dropdown"""
        if self.dropdown_visible:
            self.dropdown_frame.pack_forget()
            self.dropdown_visible = False

    def set_text(self, text: str):
        """Set search entry text"""
        self.search_var.set(text)

class WeatherCard(ctk.CTkFrame):
    """Card widget for displaying weather information"""

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
        """Add an information row to the card"""
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
    """Card for displaying daily forecast"""

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
        """Update forecast card with new data"""
        self.day_label.configure(text=day)
        self.icon_label.configure(text=icon)
        self.temp_label.configure(text=f"{temp_high}° / {temp_low}°")
        self.desc_label.configure(text=description.title())

class SettingsPanel(ctk.CTkFrame):
    """Settings panel for app configuration"""

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
        """Handle theme change"""
        theme = choice.lower()
        ctk.set_appearance_mode(theme)

    def get_settings(self) -> Dict:
        """Get current settings"""
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
    """Status bar for showing app status"""

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
        """Update status text"""
        self.status_var.set(status)

    def update_time(self):
        """Update last updated time"""
        current_time = datetime.now().strftime("%H:%M:%S")
        self.time_var.set(f"Last updated: {current_time}")
