"""
This script crawls a list of the richest bitcoin addresses and their balances
and stores the result in a CSV file.
"""

# Imports
import argparse
import logging
from datetime import date
import pyfiglet
from marx import crawler


# Configuration
DEFAULT_LIMIT = 10000
DATA_PATH = "data/"
DEFAULT_FILE_PATH = DATA_PATH + "bitcoin_balances_ddmmYYYY.csv"


def _parse_cmd_args():
    """
    This function parses the command-line arguments of the program.

    :return: The parsed command-line arguments.
    """
    parser = argparse.ArgumentParser(description='Capture connections')

    parser.add_argument(
        "--l", help=("limit of crawled bitcoin addresses. Default is " + str(DEFAULT_LIMIT)),
        default=DEFAULT_LIMIT
    )

    parser.add_argument(
        "--f", help=("path of destination file. Default is '"
                     + str(DEFAULT_FILE_PATH) + "'"),
        default=DEFAULT_FILE_PATH
    )

    args = parser.parse_args()
    return args


def _main():
    """
    This function executes the script.

    :return: None.
    """
    # Configuration
    logging.basicConfig(
        level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

    # Parsing command line args
    args = _parse_cmd_args()
    logging.debug("Command line args: %s", args)

    limit = int(args.l)
    dest_file = args.f

    # Print figlet
    banner = pyfiglet.figlet_format("MARX")
    print(banner)

    # Crawl balances
    logging.info("Crawling %d richest bitcoin addresses", limit)

    balances = crawler.crawl_richest_addresses(limit=limit)

    # Output results
    current_date = date.today()
    dest_file = dest_file.replace("ddmmYYYY", current_date.strftime("%d%m%Y"))

    logging.info("Storing results in: %s", dest_file)
    balances.to_csv(dest_file, index=False)


# Main block for execution
if __name__ == "__main__":
    _main()
