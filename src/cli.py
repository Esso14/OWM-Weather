import argparse
from colorama import Fore, Style
from main import main
import exporter
from logger import setup_logger

logger = setup_logger(__name__)

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

    # run-all: collect data and export
    subparsers.add_parser(
        "run-all",
        help="Collect weather data and export to JSON and CSV files"
    )   

    return parser

def main_cli():
    parser = create_cli()
    args = parser.parse_args()

    if args.command == "data-collect":
        main()

    elif args.command == "export-json":
        exporter.export_to_json()

    elif args.command == "export-csv":
        exporter.export_to_csv()

    elif args.command == "run-all":
        main()
        exporter.export_to_json()
        exporter.export_to_csv()

    else:
        parser.print_help()

if __name__ == "__main__":
    main_cli()