import logging
from logging.handlers import RotatingFileHandler


def setup_logger(name='weather_logger'):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if not logger.hasHandlers(): # Prevent doppelte or multiple handlers

        # Create datei-logging
        file_handler = RotatingFileHandler("logs/weather.log", maxBytes=1*1024*1024, backupCount=3)

        # Create console-logging
        console_handler = logging.StreamHandler()

        # Create formatter
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')

        # Add formatter to handlers
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # Add handler to logger
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    # A Logger per module: each module gets its own logger name, without duplicate log entries.
    logger.propagate = False 

    return logger
