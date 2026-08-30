# -*- coding: utf-8 -*-
"""
This module contains functions for scraping data from the MBS and PBS websites.
"""
import requests
import asyncio
from pathlib import Path
from typing import List

def month_range(start_month: int, end_month: int) -> List[int]:
    """
    Generates a list of months in YYYYMM format between a start and end month.

    Args:
        start_month: The starting month in YYYYMM format.
        end_month: The ending month in YYYYMM format.

    Returns:
        A list of integers representing the months.
    """
    months = []
    current_year = start_month // 100
    current_month = start_month % 100

    while (current_year * 100 + current_month) <= end_month:
        months.append(current_year * 100 + current_month)
        current_month += 1
        if current_month > 12:
            current_month = 1
            current_year += 1
    return months

async def scrape_items(item_numbers: List[str], item_months: List[int], output_dir: Path):
    """
    Scrapes MBS item data for a given list of item numbers and months.

    Args:
        item_numbers: A list of MBS item numbers to scrape.
        item_months: A list of months to scrape data for.
        output_dir: The directory to save the raw HTML files to.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    for month in item_months:
        for item_number in item_numbers:
            url = f"https://www.mbsonline.gov.au/internet/mbsonline/publishing.nsf/Content/item{item_number}-{month}"
            try:
                response = requests.get(url)
                response.raise_for_status()  # Raise an exception for HTTP errors
                file_path = output_dir / f"item_{item_number}_{month}.html"
                with open(file_path, "wb") as f:
                    f.write(response.content)
                print(f"Downloaded {url} to {file_path}")
            except requests.exceptions.RequestException as e:
                print(f"Error downloading {url}: {e}")
            await asyncio.sleep(0.1) # Be polite to the server


async def scrape_participants(participant_months: List[int], output_dir: Path):
    """
    Scrapes MBS participant data for a given list of months.

    Args:
        participant_months: A list of months to scrape data for.
        output_dir: The directory to save the raw HTML files to.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    for month in participant_months:
        url = f"https://www.mbsonline.gov.au/internet/mbsonline/publishing.nsf/Content/participants-{month}"
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for HTTP errors
            file_path = output_dir / f"participants_{month}.html"
            with open(file_path, "wb") as f:
                f.write(response.content)
            print(f"Downloaded {url} to {file_path}")
        except requests.exceptions.RequestException as e:
            print(f"Error downloading {url}: {e}")
        await asyncio.sleep(0.1) # Be polite to the server
