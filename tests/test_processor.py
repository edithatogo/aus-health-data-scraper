import pytest
from pathlib import Path
import pandas as pd
import os
from src.processor import combine_and_save_data

@pytest.fixture
def temp_dirs(tmp_path):
    raw_dir = tmp_path / "data" / "raw"
    processed_dir = tmp_path / "data" / "processed"
    raw_dir.mkdir(parents=True, exist_ok=True)
    processed_dir.mkdir(parents=True, exist_ok=True)
    return raw_dir, processed_dir

def test_combine_and_save_data(temp_dirs):
    raw_dir, processed_dir = temp_dirs
    output_filepath = processed_dir / "dataset.csv"

    # Copy sample HTML files to the temporary raw directory
    sample_item_path = Path("tests/fixtures/sample_item.html")
    sample_participant_path = Path("tests/fixtures/sample_participant.html")
    
    (raw_dir / "sample_item.html").write_bytes(sample_item_path.read_bytes())
    (raw_dir / "sample_participant.html").write_bytes(sample_participant_path.read_bytes())

    # Run the main processing function
    combine_and_save_data(str(raw_dir), str(output_filepath))

    # Assert that the output CSV file exists
    assert output_filepath.exists()

    # Read the generated CSV and perform basic assertions on its content
    df = pd.read_csv(output_filepath)
    
    # The exact assertions will depend on the content of your sample HTML files
    # and how combine_and_save_data processes them. 
    # For now, let's check if the DataFrame is not empty.
    assert not df.empty
    
    # You might want to add more specific assertions here based on your expected output
    # For example:
    # assert len(df) > 0
    # assert "ExpectedColumnName" in df.columns
