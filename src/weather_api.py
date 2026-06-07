import requests
import threading
from config import API_KEY, API_URL
from models import WeatherRecord
from datetime import datetime
from weather_cache import WeatherCache
from logger import setup_logger

logger = setup_logger(__name__)

class WeatherAPI:

    def __init__(self, api_key=API_KEY, api_url=API_URL, cache_ttl=600, cleanup_interval=300):
        self.api_key = api_key
        self.api_url = api_url
        self.cache = WeatherCache(cache_ttl=cache_ttl, cleanup_interval=cleanup_interval)

    # -----------------------------
    # API Fetch
    # -----------------------------
    def _fetch(self, lat, lon, lang):
        cached = self.cache.get_from_cache(lat, lon, lang)
        if cached:
            return cached

        params = {
            "lat": lat,
            "lon": lon,
            "appid": self.api_key,
            "units": "metric",
            "lang": lang
        }

        response = requests.get(self.api_url, params=params)
        response.raise_for_status()
        data = response.json()

        self.cache.save_to_cache(lat, lon, lang, data)
        return data
    
    # -----------------------------
    # Public API
    # -----------------------------
    def get_weather(self, lat, lon):
        try:
            # Englich data
            data_en = self._fetch(lat, lon, "en")

            # Deutsch data
            data_de = self._fetch(lat, lon, "de")

            return WeatherRecord(
                city_id=None,  # Will be set later
                description_en=data_en["weather"][0]["description"],
                description_de=data_de["weather"][0]["description"],
                temp=data_en["main"]["temp"],
                temp_min=data_en["main"]["temp_min"],
                temp_max=data_en["main"]["temp_max"],
                date=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )
        except requests.RequestException as e:
            logger.error(f"Error fetching weather data: {e}")
            return None
        
    def stop_cache_cleaner(self):
        self.cache.stop_cleaner()