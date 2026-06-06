import requests
import threading
from config import API_KEY, API_URL
from db import Database
from models import City, WeatherRecord
from datetime import datetime, timedelta
import time
from logger import setup_logger

logger = setup_logger(__name__)

class WeatherAPI:

    def __init__(self, api_key=API_KEY, api_url=API_URL, cache_ttl=600, cleanup_interval=300):
        self.api_key = api_key
        self.api_url = api_url
        self.cache = {} # Cache with keys as (lat, lon, lang): and values as (weather_data, timestamp)
        self.cache_ttl = cache_ttl # Time to live for cache entries in seconds
        self.cleanup_interval = cleanup_interval # Time interval for cache cleanup in seconds
        self._stop_cleanup = False
        self._lock = threading.Lock() # Lock for thread-safe cache access
        self._start_cleaner() # Background-Creaner starten


    # -----------------------------
    # Cache intern
    # -----------------------------
    def _get_from_cache(self, lat, lon, lang):
        key = (lat, lon, lang)
        with self._lock:
            if key in self.cache:
                timestamp, data = self.cache[key]
                if datetime.now() - timestamp < timedelta(seconds=self.cache_ttl):
                    logger.info(f"Cache hit for {key}")
                    return data
                else:
                    logger.info(f"Cache expired for {key}")
                    del self.cache[key]
        return None
    

    def _save_to_cache(self, lat, lon, lang, data):
        key = (lat, lon, lang)
        with self._lock:
            self.cache[key] = (datetime.now(), data)

    # -----------------------------
    # Background Cleaner
    # -----------------------------
    def _start_cleaner(self):
        thread = threading.Thread(target=self._cleaner_loop, daemon=True)
        thread.start()

    def _cleaner_loop(self):
        while not self._stop_cleaner:
            time.sleep(self.cleanup_interval)
            self._cleanup_cache()

    def _cleanup_cache(self):
        now = datetime.now()
        removed = 0

        with self._lock:
            keys_to_delete = [
                key for key, (timestamp, _) in self.cache.items()
                if now - timestamp > timedelta(seconds=self.cache_ttl)
            ]

            for key in keys_to_delete:
                del self.cache[key]
                removed += 1

        if removed > 0:
            logger.info(f"Cache cleanup: removed {removed} expired entries")

    def stop_cleaner(self):
        self._stop_cleaner = True

    # -----------------------------
    # API Fetch
    # -----------------------------
    def _fetch(self, lat, lon, lang):
        cached = self._get_from_cache(lat, lon, lang)
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

        self._save_to_cache(lat, lon, lang, data)
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
        