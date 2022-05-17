"""
This module contains test cases for the module marx.crawler.
"""

# Imports
import pytest
from pandas.api.types import is_numeric_dtype
from marx import crawler


# Configuration
_VALID_URL1 = "https://bitinfocharts.com/en/top-100-richest-bitcoin-addresses.html"
_VALID_URL2 = "https://bitinfocharts.com/en/top-100-richest-bitcoin-addresses-2.html"
_INVALID_URL = "https://www.google.de"


def test_crawl_richest_addresses_by_url():
    """
    Testcase for the function _crawl_richest_addresses_by_url.

    :return: None.
    """
    # Crawl first valid page
    result_frame = crawler._crawl_richest_addresses_by_url(_VALID_URL1)

    assert result_frame is not None
    assert len(result_frame) == 100

    # Check column names
    assert "rank" in result_frame.columns
    assert "address" in result_frame.columns
    assert "balance" in result_frame.columns
    assert "crawled" in result_frame.columns

    # Check ranks
    assert list(result_frame["rank"]) == list(range(1, 101))

    # Check bitcoins
    assert is_numeric_dtype(result_frame["balance"])

    # Check crawl dates
    assert len(result_frame["crawled"].unique()) == 1

    # Crawl second valid page
    result_frame = crawler._crawl_richest_addresses_by_url(_VALID_URL2)

    assert result_frame is not None
    assert len(result_frame) == 100

    # Check ranks
    assert list(result_frame["rank"]) == list(range(101, 201))

    # Check bitcoins
    assert is_numeric_dtype(result_frame["balance"])

    # Crawl invalid page
    assert crawler._crawl_richest_addresses_by_url(_INVALID_URL) is None

    # Check crawl dates
    assert len(result_frame["crawled"].unique()) == 1


def test_crawl_richest_addresses():
    """
    Testcase for the function crawl_richest_addresses.

    :return: None.
    """
    # Test valid calls
    result_frame = crawler.crawl_richest_addresses(limit=1)

    assert result_frame is not None
    assert len(result_frame) == 100

    result_frame = crawler.crawl_richest_addresses(limit=50)

    assert result_frame is not None
    assert len(result_frame) == 100

    result_frame = crawler.crawl_richest_addresses(limit=110)

    assert result_frame is not None
    assert len(result_frame) == 200

    result_frame = crawler.crawl_richest_addresses(limit=200)

    assert result_frame is not None
    assert len(result_frame) == 200

    # Test invalid calls
    with pytest.raises(AssertionError):
        crawler.crawl_richest_addresses(0)

    with pytest.raises(AssertionError):
        crawler.crawl_richest_addresses(10001)
