# WeatherPy - Advanced Weather Forecast Application

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
source venv/bin/activate  # On Windows: venv\Scripts\activate
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
Contact me : therajtiwari.1@gmail.com
**Enjoy tracking the weather with WeatherPy!** 🌤️
