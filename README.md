# OWM Weather Collector

An object‑oriented Python project that retrieves daily weather data from the **OpenWeatherMap API** for multiple German cities.  
The collected data is stored in a **SQLite database** and can be used for analytics, automation, or visualization.

---

## Features

- Fetches weater data based on latitude & longitude for:
  - Berlin
  - Stuttgart
  - Munich 
- Stores all weather data in a SQLite database
- Clean object‑oriented architecture (API client, DB layer, data models)
- Weather descriptions available in English and German
- In‑memory caching with TTL (Time-to-live)
- Background cleaner thread for expired cache entries
- Stopping the cleaner vor exemple by shut down: weather_api.stop_cleaner()
- Logging for debugging and monitoring  
- Clean and modular architecture
- JSON and CSV export  
- Easily extendable (CLI mode, history view, etc.)
- Suitable for automation via Cron or Task Scheduler

---

## Project Strukture
<pre>
OWM-Weather/
│
├── src/
│   ├── main.py
│   ├── config.py
│   ├── logger.py
│   ├── db.py
│   ├── exporter.py
│   ├── weather_api.py
│   ├── weather_cache.py
│   ├── models.py
│
├── data/
│   └── weather.db
│
├── exports/
│   └── weather.csv
│   └── weather.json
│
├── logs/
│   └── weather.log
│
├── .gitignore
├── README.md
└── requirements.txt
</pre>
---

## Database Schema

### Table: `city`

| Column     | Type    | Description           |
|------------|---------|-----------------------|
| city_id    | INTEGER | Primary key           |
| city_name  | TEXT    | Name of the city      |
| lat        | REAL    | Latitude of the city  |
| lon        | REAL    | Longitude of the city |


### Table: `weather`

| Column         | Type    | Description                            |
|----------------|---------|----------------------------------------|
| id             | INTEGER | Primary key                            |
| city_id        | INTEGER | Foreign key → `city.city_id`           |
| description_en | TEXT    | Weather description (English)          |
| description_de | TEXT    | Weather description (German)           |
| temp           | REAL    | Temperature                            |
| temp_min       | REAL    | Minimum temperature                    |
| temp_max       | REAL    | Maximum temperature                    |
| date           | TEXT    | Date of the weather record             |

---

## Installation & Setup

### 1. Clone the repository

`git clone <repo-url???>`
`cd OWM-Weather`

### 2. Install dependencies
`pip install -r requirements.txt`

### 3. Add your API key

Edit `src/config.py`:

```python
API_KEY = "DEIN_API_KEY ???"
```

### 4. Database initialization
The SQLite database is created automatically on first run.

---

## Running the Project

python `src/main.py`

This will fetch weather data for all configured cities and store it in `data/weather.db`.

---

## Automation (Cronjob Example)

To run the script every day at 07:00:

`0 7 * * * /usr/bin/python3 /pfad/zu/OWM-Weather/src/main.py >> /pfad/zu/OWM-Weather/logs/cron.log 2>&1`

---



## Technologies Used

- Python 3.x
- SQLite
- OpenWeatherMap API
- Objektorientiertes Design

---

## License

This project is free to use and can be extended as needed.

