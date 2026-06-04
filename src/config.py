from dotenv import load_dotenv
import os   

load_dotenv()

API_KEY = os.getenv("API_Key")
API_URL = os.getenv("API_URL")

CITIES = {
    1: {"name": "Berlin", "lat": 52.5200, "lon": 13.4050},
    2: {"name": "Stuttgart", "lat": 48.7833, "lon": 9.1833},
    3: {"name": "Munich", "lat": 48.1351, "lon": 11.5820}
}
