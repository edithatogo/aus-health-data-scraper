# -*- coding: utf-8 -*-
"""
Load, reshape and EDA for MBS HTML pages.
"""

import logging
import re
import io
import warnings
from pathlib import Path

import pandas as pd
from bs4 import BeautifulSoup
from tqdm import tqdm

# ------------------------------------------------------------------
# 1️⃣  Configuration
# ------------------------------------------------------------------
LOG_PATH = Path("logs/processor.log")
LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

# ------------------------------------------------------------------
# 2️⃣  Logging
# ------------------------------------------------------------------
logging.basicConfig(
    filename=LOG_PATH,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

# ------------------------------------------------------------------
# 3️⃣  Item Processing
# ------------------------------------------------------------------

STATES = {"nsw", "vic", "qld", "sa", "wa", "tas", "act", "nt"}
MON_RE = re.compile(r"^[A-Z]{3}\d{4}$")
FY_RE = re.compile(r"^\d{4}[-/]\d{2}$")
STRIP = lambda s: re.sub(r"[\s\u00A0]+", "", str(s)).lower()

def read_item_table(path: Path) -> pd.DataFrame | None:
    """
    Reads an HTML table from a given path, attempting different header configurations.

    Args:
        path: The Path object to the HTML file.

    Returns:
        A pandas DataFrame if a table is successfully read, otherwise None.
    """
    for header in ([0, 1, 2], None):
        try:
            return pd.read_html(path, header=header, flavor="lxml")[0]
        except ValueError:
            continue
    return None

def promote_item_header(df: pd.DataFrame) -> pd.DataFrame:
    """
    Promotes a row within the DataFrame to become the new header if it contains
    'gender' and 'age range' in its cells.

    Args:
        df: The input pandas DataFrame.

    Returns:
        A new DataFrame with the promoted header and rows below it, or the original
        DataFrame if no suitable header row is found.
    """
    for i, row in df.iterrows():
        cells = [str(x).strip().lower() for x in row.tolist()]
        if "gender" in cells and "age range" in cells:
            df.columns = df.iloc[i]
            return df.iloc[i + 1 :].reset_index(drop=True)
    return df

def tidy_item_html(df_raw: pd.DataFrame) -> pd.DataFrame | None:
    """
    Tidies a raw DataFrame extracted from an MBS item HTML page.

    Args:
        df_raw: The raw pandas DataFrame extracted from the HTML.

    Returns:
        A tidied pandas DataFrame, or None if the required columns are not found.
    """
    if isinstance(df_raw.columns, pd.MultiIndex):
        df_raw.columns = [
            " ".join(str(x).strip() for x in tup if str(x).strip())
            for tup in df_raw.columns
        ]
    df_raw.columns = [str(c).strip() for c in df_raw.columns]
    if not {"Gender", "Age Range"}.issubset(df_raw.columns):
        df_raw = promote_item_header(df_raw)
    if not {"Gender", "Age Range"}.issubset(df_raw.columns):
        return None
    cols = df_raw.columns.tolist()

    if "Month" in cols:
        idc = ["Gender", "Age Range", "Month"]
        vc = [c for c in cols if STRIP(c) in STATES]
        df_long = df_raw.melt(
            id_vars=idc, value_vars=vc, var_name="State", value_name="value"
        ).rename(columns={"Month": "Period"})
    else:
        idc = ["Gender", "Age Range", "State"]
        vc = [c for c in cols if MON_RE.match(STRIP(c)) or FY_RE.match(STRIP(c))]
        if not vc:
            return None
        df_long = df_raw.melt(
            id_vars=idc, value_vars=vc, var_name="Period", value_name="value"
        )

    df_long["value"] = (
        df_long["value"]
        .astype(str)
        .str.replace(r"[^0-9.\-]", "", regex=True)
        .replace("", pd.NA)
        .astype(float)
    )
    df_long = df_long.dropna(subset=["value"])
    df_long = df_long[df_long["Gender"].str.lower().isin({"male", "female"})]
    df_long = df_long[df_long["Age Range"].str.strip().str.lower() != "total"]
    df_long["Date"] = pd.to_datetime(df_long["Period"], format="%b%Y", errors="coerce")
    df_long["value"] = df_long["value"].round().astype("Int64")
    for c in ["Gender", "Age Range", "State", "Period"]:
        if c in df_long:
            df_long[c] = df_long[c].astype("category")
    return df_long

def process_items(input_dir: Path, output_path: Path):
    """
    Processes all HTML files in the input directory to extract and tidy MBS item data.
    Concatenates all processed data into a single DataFrame and saves it to a CSV file.

    Args:
        input_dir: The directory containing the raw MBS item HTML files.
        output_path: The full path to the output CSV file for processed item data.
    """
    logging.info("---- Starting Item processing ----")
    warnings.filterwarnings(
        "ignore",
        message="Passing literal html to 'read_html' is deprecated",
        category=FutureWarning,
    )

    files = sorted(input_dir.glob("*.html"))
    all_dfs = []

    for fn in tqdm(files, desc="Processing Items", unit="file"):
        with open(fn, "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f, "lxml")
        tables = soup.find_all("table")
        if not tables:
            logging.warning(f"{fn.name}: NO <table> found → SKIP")
            continue

        df0 = read_item_table(fn)
        if df0 is None:
            logging.warning(f"{fn.name}: pd.read_html(full) failed → SKIP")
        else:
            df0 = promote_item_header(df0)
            parsed = tidy_item_html(df0)
            if parsed is None or parsed.empty:
                logging.warning(f"{fn.name}: tidy_html → SKIP")
            else:
                all_dfs.append(parsed)

    if all_dfs:
        final_df = pd.concat(all_dfs, ignore_index=True)
        final_df.to_csv(output_path, index=False)
        logging.info(f"✔️  Processed {len(files)} files → {len(final_df)} rows total")
        logging.info(f"✅  Written Item CSV → {output_path}")
    else:
        logging.error("❌  No Item data processed")

    logging.info("---- Finished Item processing ----")

# ------------------------------------------------------------------
# 4️⃣  Participant Processing
# ------------------------------------------------------------------

def find_participant_table(tables: list[pd.DataFrame], fname: str) -> pd.DataFrame | None:
    """
    Identifies the main data table from a list of DataFrames extracted from a participant HTML page.

    Args:
        tables: A list of pandas DataFrames extracted from an HTML page.
        fname: The filename of the HTML page (for logging purposes).

    Returns:
        The DataFrame identified as the main data table, or None if not found.
    """
    for idx, tbl in enumerate(tables):
        cols = list(tbl.columns)
        if len(cols) > 1 and "Number of cards with" in str(cols[0]):
            logging.info(f"{fname}: selected table[{idx}] for data, shape={tbl.shape}")
            return tbl
    return None

def process_participants(input_dir: Path, output_path: Path):
    """
    Processes all HTML files in the input directory to extract and tidy MBS participant data.
    Concatenates all processed data into a single DataFrame and saves it to a CSV file.

    Args:
        input_dir: The directory containing the raw MBS participant HTML files.
        output_path: The full path to the output CSV file for processed participant data.
    """
    logging.info("---- Starting Participant processing ----")
    all_long = []
    files = sorted(input_dir.glob("std_standard_report_*.html"))
    for path in tqdm(files, desc="Processing Participants", unit="file"):
        fname = path.name
        html = path.read_text(encoding="utf-8")
        sio = io.StringIO(html)
        try:
            tables = pd.read_html(sio, flavor=["lxml", "bs4"])
        except ValueError:
            logging.warning(f"{fname}: ⚠️  No tables at all")
            continue

        data_tbl = find_participant_table(tables, fname)
        if data_tbl is None:
            logging.warning(f"{fname}: ⚠️  No data table found")
            continue

        period = fname.replace("std_standard_report_", "").replace(".html", "")
        long = data_tbl.melt(
            id_vars=[data_tbl.columns[0]], var_name="state", value_name="count"
        ).rename(columns={data_tbl.columns[0]: "cards"})

        long["count"] = (
            pd.to_numeric(
                long["count"]
                .astype(str)
                .str.replace(",", "", regex=False)
                .str.strip()
                .replace({"", None}),
                errors="coerce",
            )
            .round(0)
            .astype("Int64")
        )

        long.insert(0, "period", period)
        all_long.append(long)

    if all_long:
        df = pd.concat(all_long, ignore_index=True)
        df.to_csv(output_path, index=False)
        logging.info(f"✔️  Loaded {len(files)} files → {len(df)} rows total")
        logging.info(f"✅  Written Participant CSV → {output_path}")
    else:
        logging.error("❌  No Participant data loaded")

    logging.info("---- Finished Participant processing ----")
