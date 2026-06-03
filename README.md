# OWM Weather Collector

An object‑oriented Python project that retrieves daily weather data from the **OpenWeatherMap API** for multiple German cities.  
The collected data is stored in a **SQLite database** and can be used for analytics, automation, or visualization.

---

## Features

- Fetches weater data for:
  - Berlin
  - Aachen
  - Stuttgart
- Stores all weather data in a SQLite database
- Clean object‑oriented architecture (API client, DB layer, data models)
- Weather descriptions available in English and German
- Easily extendable (logging, caching, CLI mode, JSON export, history view, etc.)
- Suitable for automation via Cron or Task Scheduler

---

## Project Strukture

OWM-Weather/
│
├── src/
│   ├── main.py
│   ├── config.py
│   ├── db.py
│   ├── weather_api.py
│   ├── models.py
│
├── data/
│   └── weather.db
│
├── logs/
├── .gitignore
├── README.md
└── requirements.txt


---

## Database Schema

### Table: `city`

| Column     | Type    | Description        |
|------------|---------|--------------------|
| city_id    | INTEGER | Primary key        |
| city_name  | TEXT    | Name of the city   |


### Table: `weather`

| Column         | Type    | Description                           |
|----------------|---------|----------------------------------------|
| id             | INTEGER | Primary key                            |
| fk_city_id     | INTEGER | Foreign key → `city.city_id`           |
| description_en | TEXT    | Weather description (English)          |
| description_de | TEXT    | Weather description (German)           |
| temp           | REAL    | Temperature                            |
| temp_min       | REAL    | Minimum temperature                    |
| temp_max       | REAL    | Maximum temperature                    |
| date           | TEXT    | Date of the weather record             |

---

## Installation & Setup

### 1. Clone the repository

git clone <repo-url???>
cd OWM-Weather

### 2. Install dependencies
pip install -r requirements.txt

### 3. Add your API key

Edit `src/config.py`:

```python
API_KEY = "DEIN_API_KEY ???"

### 4. Database initialization
The SQLite database is created automatically on first run.

---

## Running the Project

python src/main.py

This will fetch weather data for all configured cities and store it in data/weather.db.

---

## Automation (Cronjob Example)

To run the script every day at 07:00:

0 7 * * * /usr/bin/python3 /pfad/zu/OWM-Weather/src/main.py >> /pfad/zu/OWM-Weather/logs/cron.log 2>&1

---

## Technologies Used

- Python 3.x
- SQLite
- OpenWeatherMap API
- Objektorientiertes Design

---

## License

This project is free to use and can be extended as needed.
