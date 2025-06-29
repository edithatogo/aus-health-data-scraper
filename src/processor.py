import pandas as pd
from lxml import html
import os
import glob

def process_html_file(filepath):
    """
    Reads an HTML file, extracts tables using pandas, and performs basic cleaning.
    Returns a list of DataFrames, one for each table found.
    """
    try:
        # Read HTML tables directly into a list of DataFrames
        tables = pd.read_html(filepath, flavor='lxml')
        cleaned_tables = []
        for i, df in enumerate(tables):
            # Basic cleaning: drop rows/columns that are entirely NaN
            df_cleaned = df.dropna(axis=0, how='all').dropna(axis=1, how='all')
            
            # Further cleaning/transformation would go here based on specific HTML structure
            # For example, setting proper headers, melting data, etc.
            # This is a placeholder for more complex logic.
            
            if not df_cleaned.empty:
                cleaned_tables.append(df_cleaned)
                print(f"  - Extracted and cleaned table {i+1} from {os.path.basename(filepath)}")
        return cleaned_tables
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return []

def combine_and_save_data(input_dir, output_filepath):
    """
    Processes all HTML files in the input directory, combines their data,
    and saves the result to a single CSV file.
    """
    all_dataframes = []
    html_files = glob.glob(os.path.join(input_dir, "*.html"))

    if not html_files:
        print(f"No HTML files found in {input_dir}. Skipping processing.")
        return

    print(f"Processing {len(html_files)} HTML files from {input_dir}...")
    for filepath in html_files:
        print(f"Processing file: {os.path.basename(filepath)}")
        tables = process_html_file(filepath)
        for df in tables:
            all_dataframes.append(df)

    if all_dataframes:
        # Concatenate all dataframes into a single long-form dataframe
        # This assumes a compatible schema or that each table is distinct.
        # More sophisticated merging/joining might be needed based on actual data.
        combined_df = pd.concat(all_dataframes, ignore_index=True)
        
        # Ensure the output directory exists
        output_dir = os.path.dirname(output_filepath)
        os.makedirs(output_dir, exist_ok=True)

        combined_df.to_csv(output_filepath, index=False)
        print(f"Successfully combined and saved data to {output_filepath}")
    else:
        print("No data extracted from HTML files. No CSV file generated.")

if __name__ == "__main__":
    input_raw_dir = "data/raw"
    output_processed_file = "data/processed/dataset.csv"
    
    combine_and_save_data(input_raw_dir, output_processed_file)