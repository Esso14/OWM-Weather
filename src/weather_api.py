import requests
from config import API_KEY, API_URL
from db import Database
from models import City, WeatherRecord
from datetime import datetime

class WeatherAPI:

    def __init__(self, api_key=API_KEY, api_url=API_URL):
        self.api_key = api_key
        self.api_url = api_url  

    def _fetch(self, lat, lon, lang):
        params = {
            "lat": lat,
            "lon": lon,
            "appid": self.api_key,
            "units": "metric",
            "lang": lang
        }

        response = requests.get(self.api_url, params=params)
        response.raise_for_status()
        return response.json()
    
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
            print(f"Error fetching weather data: {e}")
            return None