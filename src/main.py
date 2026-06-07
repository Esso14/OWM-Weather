from config import API_KEY, CITIES
from db import Database
from weather_api import WeatherAPI
import exporter
from logger import setup_logger

logger = setup_logger(__name__)

def main():
    try:
        logger.info("Starting OWM Weather Collector...")

        # Initialize the database and API client
        db = Database()
        db.init_cities_from_config() # Ensure cities from config are in the database
        api = WeatherAPI()

        # Fetch and store weather data for each city
        for city_id, city in CITIES.items():
            try:

                logger.info(f"Fetching weather data for {city['name']}...")

                weather_data = api.get_weather(city["lat"], city["lon"])

                if weather_data is None:
                    logger.error(f"Failed to fetch weather data for {city['name']}.")
                    continue        

                weather_data.city_id = city_id
                db.insert_weather_record(weather_data)

                logger.info(f"Weather data for {city['name']} stored successfully.")

            except Exception as e:
                logger.exception(f"Error processing city {city['name']}: {e}")
        
        logger.info("Weather updated.")

    except Exception as e:
        logger.exception(f"An error occurred: {e}")
 

if __name__ == "__main__":
    main()
