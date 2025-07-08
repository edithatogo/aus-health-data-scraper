import pandas as pd
from lxml import html
import os
import glob

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
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return []

def combine_and_save_data(input_dir: str, output_filepath: str):
    """Processes all HTML files in a directory, combines the data, and saves to CSV.

    This function iterates through all `.html` files in the specified input
    directory. It calls `process_html_file` for each file, concatenates all
    the extracted tables into a single DataFrame, and saves it as a CSV file.

    Args:
        input_dir: The path to the directory containing the raw HTML files.
        output_filepath: The path where the final combined CSV file will be saved.
    """
    all_dataframes = []
    # Use glob to find all HTML files, supporting various extensions
    html_files = glob.glob(os.path.join(input_dir, "*.html")) + \
                 glob.glob(os.path.join(input_dir, "*.htm"))

    if not html_files:
        print(f"No HTML files found in {input_dir}. Skipping processing.")
        return

    print(f"Processing {len(html_files)} HTML files from {input_dir}...")
    for filepath in html_files:
        print(f"Processing file: {os.path.basename(filepath)}")
        tables = process_html_file(filepath)
        # Extend the list of dataframes with the tables from the current file
        all_dataframes.extend(tables)

    if all_dataframes:
        # Concatenate all dataframes. `ignore_index=True` creates a new index.
        combined_df = pd.concat(all_dataframes, ignore_index=True)

        # Ensure the output directory exists before saving
        output_dir = os.path.dirname(output_filepath)
        os.makedirs(output_dir, exist_ok=True)

        combined_df.to_csv(output_filepath, index=False)
        print(f"Successfully combined and saved data to {output_filepath}")
    else:
        print("No data was extracted from the HTML files. No CSV file was generated.")

if __name__ == "__main__":
    input_raw_dir = "data/raw"
    output_processed_file = "data/processed/dataset.csv"
    
    combine_and_save_data(input_raw_dir, output_processed_file)