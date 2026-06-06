import sqlite3
from models import City, WeatherRecord
from config import CITIES
from logger import setup_logger

logger = setup_logger(__name__)

class Database:
    def __init__(self, db_path="data/weather.db"):
        self.db_path = db_path
        self._create_tables()

    def _connect(self):
        return sqlite3.connect(self.db_path)
    
    def _create_tables(self):
        conn = self._connect()
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cities (
                city_id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                lat REAL,
                lon REAL
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS weather_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                city_id INTEGER,
                description_en TEXT,
                description_de TEXT,
                temp REAL,
                temp_min REAL,
                temp_max REAL,
                date TEXT,
                FOREIGN KEY(city_id) REFERENCES cities(city_id)
            )
        ''')

        conn.commit()
        conn.close()

    
    def insert_city(self, city: City):
        conn = self._connect()
        cursor = conn.cursor()

        cursor.execute('''
            INSERT OR REPLACE INTO cities (city_id, name, lat, lon) 
            VALUES (?, ?, ?, ?)
        ''', (city.city_id, city.name, city.lat, city.lon))

        conn.commit()
        conn.close()

    
    def init_cities_from_config(self):
        conn = self._connect()
        cursor = conn.cursor()

        # Alle vorhandenen IDs laden
        cursor.execute("SELECT city_id FROM cities")
        existing_ids = {row[0] for row in cursor.fetchall()}

        for city_id, data in CITIES.items():
            if city_id in existing_ids:
                logger.info(f"City already exists, skipping: {data['name']}")
                continue

            city = City(
                city_id=city_id,
                name=data["name"],
                lat=data["lat"],
                lon=data["lon"]
            )

            cursor.execute("""
                INSERT INTO cities (city_id, name, lat, lon)
                VALUES (?, ?, ?, ?)
            """, (city.city_id, city.name, city.lat, city.lon))

            logger.info(f"City inserted: {city.name} ({city.lat}, {city.lon})")

        conn.commit()
        conn.close()


    def insert_weather_record(self, record: WeatherRecord):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO weather_records (city_id, description_en, description_de, temp, temp_min, temp_max, date) 
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            record.city_id, 
            record.description_en, 
            record.description_de, 
            record.temp, 
            record.temp_min, 
            record.temp_max, 
            record.date
        ))

        logger.info("Weather record inserted successfully.")
        
        conn.commit()
        conn.close()

    def get_all_weather(self):
        conn = self._connect()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT 
                w.city_id,
                c.name AS city_name,
                w.description_en,
                w.description_de,
                w.temp,
                w.temp_min,    
                w.temp_max, 
                w.date
            FROM weather_records w
            JOIN cities c ON w.city_id = c.city_id
            ORDER BY w.date DESC
        ''')

        rows = cursor.fetchall()
        conn.close()

        return [
            {
                "city_id": row[0],
                "name": row[1],
                "description_en": row[2],
                "description_de": row[3],
                "temp": row[4],
                "temp_min": row[5],
                "temp_max": row[6],
                "date": row[7]
            }
            for row in rows
        ]
    
    def get_all_weather_grouped(self):
        conn = self._connect()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT 
                w.city_id,
                c.name AS city_name,
                w.description_en,
                w.description_de,
                w.temp,
                w.temp_min,    
                w.temp_max, 
                w.date
            FROM weather_records w
            JOIN cities c ON w.city_id = c.city_id
            ORDER BY c.name, w.date DESC
        ''')

        rows = cursor.fetchall()
        conn.close()

        grouped_data = {}

        for row in rows:
            city_name = row[1]
            record = {
                "city_id": row[0],
                "name": city_name,
                "description_en": row[2],
                "description_de": row[3],
                "temp": row[4],
                "temp_min": row[5],
                "temp_max": row[6],
                "date": row[7]
            }
            if city_name not in grouped_data:
                grouped_data[city_name] = []

            grouped_data[city_name].append(record)

        return grouped_data
    