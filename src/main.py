import cli
import logger

logger = logger.setup_logger("main")

def main():
    logger.info("Starting OWM Weather Collector...")
    try:
        cli.main_cli()
    except Exception as e:
        logger.error("Fatal error in main_cli")
        raise

if __name__ == "__main__":
    main()
    