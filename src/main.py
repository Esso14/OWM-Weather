from config import API_KEY, CITIES
from db import Database
from weather_api import WeatherAPI
from models import City, weatherRecord

def main():
    print("Starting OWM Weather Collector...")

    # Initialize the database and API client
    db = Database()
    api = WeatherAPI()

    # Fetch and store weather data for each city
    for city_id, city in CITIES.items():
        print(f"Fetching weather data for {city['name']}...")

        weather_data = api.get_weather(city["lat"], city["lon"])

        if weather_data is None:
            print(f"Failed to fetch weather data for {city['name']}.")
            continue        

        weather_data.city_id = city_id
        db.insert_weather_record(weather_data)

        print(f"Weather data for {city['name']} stored successfully.")

    print("Weather updated.")


if __name__ == "__main__":
    main()
