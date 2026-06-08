import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
from logger import setup_logger

logger = setup_logger(__name__)

def plot_history(city_name, records, save_path=None):
    if not records:
        logger.warning(f"No weather records found for city: {city_name}")
        return

    # Convert date strings to datetime objects and extract temperatures
    dates = [datetime.strptime(record["date"], "%Y-%m-%d %H:%M:%S") for record in records]
    temps = [record["temp"] for record in records]
    temps_min = [record["temp_min"] for record in records]
    temps_max = [record["temp_max"] for record in records]

    # Create the plot
    plt.figure(figsize=(12, 6))
    plt.plot(dates, temps, label="Temperature", color="orange", linewidth=2, marker='o')
    plt.plot(dates, temps_min, label="Min Temperature", color="blue", linestyle='--')
    plt.plot(dates, temps_max, label="Max Temperature", color="red", linestyle='--')

    # Format the x-axis to show dates nicely
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=1))
    plt.gcf().autofmt_xdate()  # Rotate date labels

    plt.title(f"Temperature History for {city_name}")
    plt.xlabel("Date")
    plt.ylabel("Temperature (°C)")
    #plt.xticks(rotation=45)
    plt.grid(True, linestyle=':', alpha=0.5)
    plt.legend()

    plt.show()