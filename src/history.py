from db import Database
import plotter
import logger

logger = logger.setup_logger(__name__)

#-----------------------------------------------------------------------#
# Fetch and display historical weather data for a specific city         #
#-----------------------------------------------------------------------#
#------------------------------------#
#  Day history                       #
#------------------------------------#
def day_history(args):
    db = Database()
    logger.info(f"Fetching historical weather data for city: {args.city}")
    records = db.get_history_records(args.city)

    if args.plot:
        plotter.plot_history(args.city, records)
    else:
        for record in records:
            print(f"{record['date']}: {record['temp']}°C (Min: {record['temp_min']}°C, Max: {record['temp_max']}°C)")


#------------------------------------#
#  ToDo: Week history                #
#------------------------------------#