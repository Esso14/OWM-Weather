from config import API_KEY, CITIES
from db import Database
from weather_api import WeatherAPI
from models import City, weatherRecord

def main():
    print("Starting OWM Weather Collector...")

    # Initialize the database and API client
    db = Database()
    api = WeatherAPI(API_KEY)

    # Create tables if they don't exist
    # db.create_tables()

    # Fetch and store weather data for each city
    for city_id, name in CITIES.items():
        city = City(city_id, name)
        db.insert_city(city)

        weather_data = api.get_weather(name)

        if weather_data is None:
            print(f"Failed to fetch weather data for {name}.")
            continue        

        record = weatherRecord(
            city.id,
            weather_data["description_en"],
            weather_data["description_de"],
            weather_data["temp"],
            weather_data["temp_min"],
            weather_data["temp_max"],
            weather_data["date"]
        )

        db.insert_weather(record)
        print("Weather updated.")

if __name__ == "__main__":
    main()
