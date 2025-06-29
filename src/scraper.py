# -*- coding: utf-8 -*-
"""
Async bulk-download of MBS HTML pages.
"""

import asyncio
import logging
from pathlib import Path

import aiohttp
import aiofiles
import pandas as pd
from tqdm.asyncio import tqdm_asyncio

# ------------------------------------------------------------------
# 1️⃣  Configuration
# ------------------------------------------------------------------
MAX_CONCURRENCY = 10
POLITENESS_DELAY = 0.3
REQUEST_TIMEOUT = aiohttp.ClientTimeout(total=30)

# ------------------------------------------------------------------
# 2️⃣  Logging
# ------------------------------------------------------------------
LOG_PATH = Path("logs/scraper.log")
LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    filename=LOG_PATH,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

# ------------------------------------------------------------------
# 3️⃣  Helpers
# ------------------------------------------------------------------
def month_range(start_yyymm: int, end_yyymm: int) -> list[str]:
    """
    Generates a list of YYYYMM strings representing a range of months.

    Args:
        start_yyymm: The starting month in YYYYMM format (e.g., 199307 for July 1993).
        end_yyymm: The ending month in YYYYMM format (e.g., 202504 for April 2025).

    Returns:
        A list of strings, where each string is a month in YYYYMM format.
    """
    y, m = divmod(start_yyymm, 100)
    y_end, m_end = divmod(end_yyymm, 100)
    out = []
    while (y, m) <= (y_end, m_end):
        out.append(f"{y}{m:02d}")
        m += 1
        if m == 13:
            y, m = y + 1, 1
    return out

# ------------------------------------------------------------------
# 4️⃣  Scraping Functions
# ------------------------------------------------------------------

async def fetch_one(session: aiohttp.ClientSession, url: str, out_path: Path) -> None:
    """
    Downloads a single URL and writes the content to a specified file path.
    Skips download if the file already exists (cached).

    Args:
        session: An aiohttp client session for making HTTP requests.
        url: The URL to download.
        out_path: The Path object where the downloaded content will be saved.
    """
    if out_path.exists():
        logging.info("SKIP  %s", out_path.name)
        return

    sem = asyncio.Semaphore(MAX_CONCURRENCY)
    async with sem:
        await asyncio.sleep(POLITENESS_DELAY)
        try:
            async with session.get(url) as resp:
                if resp.status != 200:
                    logging.warning("FAIL  %s → HTTP %s", out_path.name, resp.status)
                    return
                html = await resp.text()
        except Exception as exc:
            logging.error("ERR   %s → %s", out_path.name, exc)
            return

    async with aiofiles.open(out_path, "w", encoding="utf-8") as f:
        await f.write(html)
    logging.info("OK    %s (%.0f KiB)", out_path.name, len(html) / 1024)

async def scrape_items(item_numbers: list[int], months: list[str], output_dir: Path) -> None:
    """
    Scrapes MBS item data for a given list of item numbers and months.

    Args:
        item_numbers: A list of integer MBS item numbers to scrape.
        months: A list of YYYYMM strings representing the months to scrape data for.
        output_dir: The directory where the scraped HTML files will be saved.
    """
    logging.info("---- Starting MBS Item scrape ----")
    output_dir.mkdir(parents=True, exist_ok=True)
    url_tmpl = (
        "https://medicarestatistics.humanservices.gov.au/SASStoredProcess/guest"
        "?_PROGRAM=SBIP%3A%2F%2FMETASERVER%2FShared+Data%2Fsasdata%2Fprod%2FVEA0032"
        "%2FSAS.StoredProcess%2Fstatistics%2Fmbs_item_age_gender_report"
        "&group={item}&VAR=services&STAT=count&RPT_FMT=by+time+period+and+state"
        "&PTYPE=month&START_DT={date}&END_DT={date}"
    )

    async with aiohttp.ClientSession(timeout=REQUEST_TIMEOUT) as sess:
        tasks = []
        for item in item_numbers:
            for ym in months:
                url = url_tmpl.format(item=item, date=ym)
                out_path = output_dir / f"Item_{item}_age_gender_{ym}.html"
                tasks.append(fetch_one(sess, url, out_path))
        await tqdm_asyncio.gather(*tasks, desc="Downloading Items", unit="file")
    logging.info("---- Finished MBS Item scrape ----")

async def scrape_participants(months: list[str], output_dir: Path) -> None:
    """
    Scrapes MBS participant data for a given list of months.

    Args:
        months: A list of YYYYMM strings representing the months to scrape data for.
        output_dir: The directory where the scraped HTML files will be saved.
    """
    logging.info("---- Starting MBS Participant scrape ----")
    output_dir.mkdir(parents=True, exist_ok=True)
    url_tmpl = (
        "https://medicarestatistics.humanservices.gov.au/SASStoredProcess/guest"
        "?action=execute"
        "&_PROGRAM=SBIP://METASERVER/Shared%20Data/sasdata/prod/VEA0032/"
        "SAS.StoredProcess/statistics/std_standard_report"
        "&start_dt={date}"
        "&ptype=month"
        "&end_dt={date}"
        "&VAR=Services"
        "&RPT_FMT=table2.2"
    )

    async with aiohttp.ClientSession(timeout=REQUEST_TIMEOUT) as sess:
        tasks = []
        for ym in months:
            url = url_tmpl.format(date=ym)
            out_path = output_dir / f"std_standard_report_{ym}.html"
            tasks.append(fetch_one(sess, url, out_path))
        await tqdm_asyncio.gather(*tasks, desc="Downloading Participants", unit="file")
    logging.info("---- Finished MBS Participant scrape ----")
