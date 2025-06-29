# -*- coding: utf-8 -*-
"""
Main entry point for the MBS scraper and processor.
"""

import asyncio
from pathlib import Path

import pandas as pd

from scraper import scrape_items, scrape_participants, month_range
from processor import process_items, process_participants

def main():
    """
    Main function to orchestrate the scraping and processing of MBS data.

    This function reads configuration, initiates the scraping of both item and
    participant data, and then processes the raw HTML files into structured CSVs.
    """
    # ------------------------------------------------------------------
    # 1️⃣  Configuration
    # ------------------------------------------------------------------
    item_file_path = Path("data/source/MBS - 2024.07 - Group P7 (Genetics).xlsx")
    items_raw_dir = Path("data/raw/items")
    participants_raw_dir = Path("data/raw/participants")
    processed_dir = Path("data/processed")

    start_month_items = 199307
    end_month_items = 202504
    start_month_participants = 199702
    end_month_participants = 202506

    # ------------------------------------------------------------------
    # 2️⃣  Scraping
    # ------------------------------------------------------------------
    item_numbers = pd.read_excel(item_file_path)["ItemNum"].unique().tolist()
    item_months = month_range(start_month_items, end_month_items)
    participant_months = month_range(start_month_participants, end_month_participants)

    asyncio.run(scrape_items(item_numbers, item_months, items_raw_dir))
    asyncio.run(scrape_participants(participant_months, participants_raw_dir))

    # ------------------------------------------------------------------
    # 3️⃣  Processing
    # ------------------------------------------------------------------
    process_items(items_raw_dir, processed_dir)
    process_participants(participants_raw_dir, processed_dir)

if __name__ == "__main__":
    main()
