import argparse
from colorama import Fore, Style
import fetch
import history
import exporter

import logger

logger = logger.setup_logger(__name__)

def create_cli():
    parser = argparse.ArgumentParser(
        description=f"{Fore.CYAN}OWM Weather Collector CLI{Style.RESET_ALL}"
    )

    subparsers = parser.add_subparsers(dest="command")

    # Run the main weather collection process
    subparsers.add_parser(
        "data-collect", 
        help="Fetch and store weather data for all configured cities"
    )

    # Export JSON
    subparsers.add_parser(
        "export-json",
        help="Export weather data to JSON file"
    )
    # Export CSV
    subparsers.add_parser(
        "export-csv",
        help="Export weather data to CSV file"
    )

    # HISTORY
    history = subparsers.add_parser("history", help="Show historical weather data for a specific city")
    history.add_argument("--city", required=True)
    history.add_argument("--plot", action="store_true")


    # run-all: collect data and export
    subparsers.add_parser(
        "run-all",
        help="Collect weather data, export to JSON and CSV files und then show historical data for a specific city"
    )   

    return parser


def main_cli():
    parser = create_cli()
    args = parser.parse_args()

    if args.command == "data-collect":
        fetch.fetch_data()

    elif args.command == "export-json":
        exporter.export_to_json()

    elif args.command == "export-csv":
        exporter.export_to_csv()

    elif args.command == "history":
        history.day_history(args)
        
    elif args.command == "run-all":
        fetch.fetch_data()
        exporter.export_to_json()
        exporter.export_to_csv()

    else:
        parser.print_help()

#if __name__ == "__main__":
    #main_cli()
