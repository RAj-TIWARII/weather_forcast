#!/usr/bin/env python3
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
        print("   venv\\Scripts\\activate  # Windows")
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
