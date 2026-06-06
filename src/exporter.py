import json
import csv
import os
from db import Database

from logger import setup_logger

logger = setup_logger(__name__)

#------------------------------#
# JSON-Export-Funktionen.      #
#------------------------------#
def export_to_json(path="exports/weather.json", grouped=True):
    db = Database()

    if grouped:
        data = db.get_all_weather_grouped()
    else:
        data = db.get_all_weather()     

    os.makedirs(os.path.dirname(path), exist_ok=True) # Ensure the directory exists    
 
    try:
        with open(path, "w", encoding="utf-8") as json_file:
            json.dump(data, json_file, indent=4, ensure_ascii=False)
            
        logger.info(f"JSON export saved to {path}")

    except Exception as e:
        logger.exception(f"Failed to export data to JSON: {e}")

#------------------------------#
# CSV-Export-Funktionen.       #
#------------------------------#
def export_to_csv(path="exports/weather.csv"):
    db = Database()
    grouped_data = db.get_all_weather_grouped()

    os.makedirs(os.path.dirname(path), exist_ok=True) # Ensure the directory exists

    try:
        with open(path, "w", encoding ="utf-8", newline="") as cvs_file:
            writer = csv.writer(cvs_file)

            # Write header
            writer.writerow([
                "city_id",
                "city_name",
                "description_en",
                "description_de",
                "temp",
                "temp_min",
                "temp_max",
                "date"
            ])

            # Write data
            for city_name, records in grouped_data.items():
                for record in records:
                    writer.writerow([
                        record["city_id"],
                        record["name"],
                        record["description_en"],
                        record["description_de"],
                        record["temp"],
                        record["temp_min"],
                        record["temp_max"],
                        record["date"]
                    ])

        logger.info(f"CSV export saved to {path}")

    except Exception as e:
        logger.exception(f"Failed to export data to CSV: {e}")


