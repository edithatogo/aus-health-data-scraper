import glob
import os
import xml.etree.ElementTree as ET
from pathlib import Path

import pandas as pd
from lxml.etree import ParserError, XMLSyntaxError


def process_mbs_xml(file_path: Path) -> list[dict]:
    """
    Parses an MBS XML file and extracts all items belonging to the "P7" group.

    Args:
        file_path: The path to the MBS XML file.

    Returns:
        A list of dictionaries, where each dictionary represents a "P7" item.
    """
    tree = ET.parse(file_path)
    root = tree.getroot()
    
    p7_items = []
    for item in root.findall("./item"):
        group = item.find("Group")
        if group is not None and group.text == "P7":
            item_data = {}
            for child in item:
                item_data[child.tag] = child.text
            p7_items.append(item_data)
            
    return p7_items

def combine_and_save_data(raw_data_dir: Path, processed_data_dir: Path):
    """Processes all HTML and XML files in a directory, combines the data, and saves to CSV.

    This function iterates through all `.html`, `.htm`, and `.xml` files in the
    specified input directory. It calls the appropriate processing function
    for each file type, concatenates all the extracted data into a single
    DataFrame, and saves it as a CSV file.

    Args:
        raw_data_dir: The path to the directory containing the raw data files.
        processed_data_dir: The path where the final combined CSV file will be saved.
    """
    all_dataframes = []
    # Use glob to find all supported files
    file_paths = glob.glob(os.path.join(raw_data_dir, "*.html")) + \
                 glob.glob(os.path.join(raw_data_dir, "*.htm")) + \
                 glob.glob(os.path.join(raw_data_dir, "*.xml"))

    if not file_paths:
        print(f"No HTML or XML files found in {raw_data_dir}. Skipping processing.")
        return

    print(f"Processing {len(file_paths)} files from {raw_data_dir}...")
    for filepath in file_paths:
        file_path_obj = Path(filepath)
        print(f"Processing file: {file_path_obj.name}")
        if file_path_obj.suffix in ['.html', '.htm']:
            tables = process_html_file(filepath)
            all_dataframes.extend(tables)
        elif file_path_obj.suffix == '.xml':
            xml_data = process_mbs_xml(file_path_obj)
            if xml_data:
                df = pd.DataFrame(xml_data)
                all_dataframes.append(df)
                print(f"  - Extracted {len(df)} items from {file_path_obj.name}")

    if all_dataframes:
        # Concatenate all dataframes. `ignore_index=True` creates a new index.
        combined_df = pd.concat(all_dataframes, ignore_index=True)

        # Ensure the output directory exists before saving
        processed_data_dir.mkdir(parents=True, exist_ok=True)
        output_filepath = processed_data_dir / "dataset.csv"

        combined_df.to_csv(output_filepath, index=False)
        print(f"Successfully combined and saved data to {output_filepath}")
    else:
        print("No data was extracted from the files. No CSV file was generated.")


def process_html_file(filepath: str) -> list[pd.DataFrame]:
    """Reads a single HTML file, extracts all tables, and cleans them.

    This function uses pandas to find and parse all <table> elements within the
    HTML file. It performs a basic cleaning by removing rows and columns that
    are entirely empty.

    Note:
        More specific cleaning logic may be required depending on the exact
        structure of the source HTML tables.

    Args:
        filepath: The absolute or relative path to the HTML file.

    Returns:
        A list of pandas DataFrames, where each DataFrame represents a
        cleaned table found in the file. Returns an empty list if no tables
        are found or if an error occurs.
    """
    try:
        # Use lxml for parsing efficiency
        tables = pd.read_html(filepath, flavor='lxml')
        cleaned_tables = []
        for i, df in enumerate(tables):
            # Basic cleaning: drop rows/columns that are entirely NaN
            df_cleaned = df.dropna(axis=0, how='all').dropna(axis=1, how='all')

            if not df_cleaned.empty:
                cleaned_tables.append(df_cleaned)
                print(f"  - Extracted and cleaned table {i+1} from {os.path.basename(filepath)}")
        return cleaned_tables
    except (ValueError, OSError, ParserError, XMLSyntaxError) as e:
        print(f"Error processing {filepath}: {e}")
        return []
