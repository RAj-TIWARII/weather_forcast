
import requests
import json
import time
from typing import Dict, Optional, Tuple
from .config import OPENWEATHER_API_KEY, OPENWEATHER_BASE_URL, CACHE_DIR, CACHE_DURATION

class WeatherAPIClient:
    """Client for fetching weather data from OpenWeatherMap API"""

    def __init__(self):
        self.api_key = OPENWEATHER_API_KEY
        self.base_url = OPENWEATHER_BASE_URL
        self.cache = {}

    def _get_cache_key(self, city: str, units: str) -> str:
        """Generate cache key for storing weather data"""
        return f"{city.lower()}_{units}"

    def _is_cache_valid(self, timestamp: float) -> bool:
        """Check if cached data is still valid"""
        return time.time() - timestamp < CACHE_DURATION

    def get_current_weather(self, city: str, units: str = "metric") -> Optional[Dict]:
        """
        Fetch current weather for a city

        Args:
            city: City name
            units: Temperature units (metric, imperial, kelvin)

        Returns:
            Weather data dictionary or None if error
        """
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
        """
        Fetch 5-day weather forecast for a city

        Args:
            city: City name
            units: Temperature units (metric, imperial, kelvin)

        Returns:
            Forecast data dictionary or None if error
        """
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
        """
        Search for cities by name

        Args:
            query: Search query
            limit: Maximum number of results

        Returns:
            List of city data dictionaries
        """
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
