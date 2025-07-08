# -*- coding: utf-8 -*-
"""
Main entry point for the MBS scraper and processor.
"""

import asyncio
from pathlib import Path

from scraper import scrape_items, scrape_participants, month_range
from processor import combine_and_save_data

def main():
    """
    Main function to orchestrate the scraping and processing of MBS data.

    This function reads configuration, initiates the scraping of both item and
    participant data, and then processes the raw HTML files into structured CSVs.
    """
    # ------------------------------------------------------------------
    # 1️⃣  Configuration
    # ------------------------------------------------------------------
    # Using dummy item numbers for demonstration as the excel file is not available
    item_numbers = ["104", "205"]
    raw_data_dir = Path("data/raw")
    processed_file = Path("data/processed/dataset.csv")

    start_month_items = 202401
    end_month_items = 202402
    start_month_participants = 202401
    end_month_participants = 202402

    # ------------------------------------------------------------------
    # 2️⃣  Scraping
    # ------------------------------------------------------------------
    item_months = month_range(start_month_items, end_month_items)
    participant_months = month_range(start_month_participants, end_month_participants)

    asyncio.run(scrape_items(item_numbers, item_months, raw_data_dir))
    asyncio.run(scrape_participants(participant_months, raw_data_dir))

    # ------------------------------------------------------------------
    # 3️⃣  Processing
    # ------------------------------------------------------------------
    combine_and_save_data(str(raw_data_dir), str(processed_file))

if __name__ == "__main__":
    main()
