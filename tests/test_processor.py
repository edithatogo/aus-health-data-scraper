import shutil
import tempfile
from pathlib import Path

import pandas as pd
import pytest

from src.processor import combine_and_save_data, process_mbs_xml


@pytest.fixture
def temp_data_dirs():
    # Create a temporary directory
    temp_dir = tempfile.mkdtemp()
    raw_dir = Path(temp_dir) / "raw"
    processed_dir = Path(temp_dir) / "processed"
    raw_dir.mkdir()
    processed_dir.mkdir()
    yield raw_dir, processed_dir
    # Clean up the temporary directory
    shutil.rmtree(temp_dir)


def test_combine_and_save_data(temp_data_dirs):
    raw_dir, processed_dir = temp_data_dirs
    fixtures_dir = Path("tests/fixtures")

    # Copy sample files to the temporary raw directory
    shutil.copy(fixtures_dir / "sample_item.html", raw_dir)
    shutil.copy(fixtures_dir / "sample_participant.html", raw_dir)
    shutil.copy(fixtures_dir / "sample_mbs.xml", raw_dir)

    # Run the processor
    combine_and_save_data(raw_dir, processed_dir)

    # Check that the output file was created and is not empty
    output_file = processed_dir / "dataset.csv"
    assert output_file.exists()
    assert output_file.stat().st_size > 0

    # Check the content of the CSV
    df = pd.read_csv(output_file)
    # Expect 3 rows from sample_item, 1 from sample_participant, and 1 from sample_mbs
    assert len(df) == 5
    # Check for a key column from the XML data
    assert "ItemNum" in df.columns
    # Check for a key column from the HTML data (assuming column names are parsed)
    # Note: Column names from HTML tables can be unpredictable. A better check
    # might be to inspect the values. For now, we'll check for a known value.
    assert "Male" in df.to_string() # Check if a known value exists
    assert "73329" in df["ItemNum"].to_string() # Check for the MBS item number

def test_process_mbs_xml():
    """
    Tests that the process_mbs_xml function correctly parses P7 items.
    """
    fixture_path = Path("tests/fixtures/sample_mbs.xml")
    p7_items = process_mbs_xml(fixture_path)
    
    # There is one "P7" item in the sample file
    assert len(p7_items) == 1
    
    # Check that the extracted item has the correct data
    item = p7_items[0]
    assert item["ItemNum"] == "73329"
    assert item["Group"] == "P7"
    assert item["Category"] == "6"
