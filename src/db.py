import sqlite3
from models import City, WeatherRecord
from datetime import datetime

class Database:
    def __init__(self, db_path="data/weather.db"):
        self.db_path = db_path
        self._create_tables()

    def _connect(self):
        return sqlite3.connect(self.db_path)
    
    def _create_tables(self):
        with self._connect() as conn:
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
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO cities (city_id, name, lat, lon) 
                VALUES (?, ?, ?, ?)
            ''', (city.city_id, city.name, city.lat, city.lon))

            conn.commit()
            conn.close()

    
    def insert_weather_record(self, record: WeatherRecord):
        with self._connect() as conn:
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

            conn.commit()
            conn.close()

