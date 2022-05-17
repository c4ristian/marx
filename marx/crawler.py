"""
This module crawls a list of the richest bitcoin addresses from the internet.
"""

# Imports
from datetime import date
import logging
import bs4
import pandas as pd
import requests


# Configuration
FIRST_URL = "https://bitinfocharts.com/en/top-100-richest-bitcoin-addresses.html"
SECOND_URL = "https://bitinfocharts.com/en/top-100-richest-bitcoin-addresses-X.html"


def _parse_balance(balance: str) -> float:
    """
    This function parses a certain bitcoin balance.

    :param balance: The balance as str.
    :return: The balance as float.
    """
    index = balance.find("BTC")
    btc_str = balance[:index].replace(",", "")
    return float(btc_str)


def _parse_table(soup: bs4.BeautifulSoup, table_name: str) -> pd.DataFrame:
    """
    This function parses a table of bitcoin addresses and their balances stored
    in a specific HTML document.

    :param soup: The HTML document as BeautifulSoup object.
    :param table_name: The name/id of the table.
    :return: A data frame with the bitcoin addresses.
    """
    result_frame = None

    # Find table in document
    table = soup.find(
        lambda tag: tag.name == 'table' and tag.has_attr('id') and tag['id'] == table_name)

    # Parse table, if exists
    if table:
        rank = []
        address = []
        balance = []

        # Try to find table body
        table_body = table.find('tbody')

        # If it is not defined, work with the table element
        if not table_body:
            table_body = table

        rows = table_body.findAll(lambda tag: tag.name == 'tr')

        # Parse rows
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]

            rank.append(cols[0])
            address.append(cols[1])
            balance.append(cols[2])

        # Create data frame with results
        result_frame = pd.DataFrame({
            "rank": rank,
            "address": address,
            "balance": balance,
            "crawled": date.today()
        })

        # Perform data transformations
        result_frame["rank"] = result_frame["rank"].astype("int64")
        result_frame["balance"] = result_frame["balance"].apply(
            _parse_balance)

    return result_frame


def _crawl_richest_addresses_by_url(url: str) -> pd.DataFrame:
    """
    This function crawls a data frame with the richest bitcoin addresses
    and their balances from a specific website.

    :param url: The URL of the website.
    :return: A data frame with the addresses and their balances.
    """
    # Get website
    logging.info("Crawling site %s", url)

    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.content, 'html.parser')

    # Parse tables
    address_frame = _parse_table(soup, "tblOne")

    current_index = 2
    table_name = "tblOneX"

    while (new_frame := _parse_table(soup, table_name.replace(
            "X", str(current_index)))) is not None:
        address_frame = pd.concat([address_frame, new_frame])
        current_index += 1

    return address_frame


def crawl_richest_addresses(limit: int) -> pd.DataFrame:
    """
    This function crawls a data frame with the richest bitcoin addresses
    and their balances from the internet.

    The addresses are crawled in batches of hundred. The actual crawled number might
    therefore lie above the limit, if it is not a multiple of hundred. The limit value
    must be greater than zero and less than or equal to 10000.

    :param limit: The limit of crawled addresses.
    :return: A data frame with the addresses and their balances.
    """
    assert 0 < limit <= 10000, "Condition 0 < limit < 10000 violated"

    balance_frame = _crawl_richest_addresses_by_url(FIRST_URL)
    page_index = 2

    while int(balance_frame["rank"].max()) < limit:
        next_url = SECOND_URL.replace("X", str(page_index))
        new_frame = _crawl_richest_addresses_by_url(next_url)
        balance_frame = pd.concat([balance_frame, new_frame])
        page_index += 1

    return balance_frame.reset_index(drop=True)
