import threading
import time
from datetime import datetime, timedelta
from logger import setup_logger

logger = setup_logger(__name__)

class WeatherCache:
    def __init__(self, cache_ttl=600, cleanup_interval=300):
        self.cache = {} # Cache with keys as (lat, lon, lang): and values as (weather_data, timestamp)
        self.cache_ttl = cache_ttl # Time to live for cache entries in seconds
        self.cleanup_interval = cleanup_interval # Time interval for cache cleanup in seconds
        self._stop_cleaner = False
        self._lock = threading.Lock() # Lock for thread-safe cache access
        self._start_cleaner() # Start background cleanup thread

    # -----------------------------
    # Cache intern
    # -----------------------------
    def get_from_cache(self, lat, lon, lang):
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
    

    def save_to_cache(self, lat, lon, lang, data):
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

    # Stop the cleaner thread gracefully: weather_api.stop_cleaner() in main.py
    def stop_cleaner(self):
        self._stop_cleaner = True