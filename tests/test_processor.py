import pytest
from pathlib import Path
import pandas as pd
import io
from src.processor import process_items, process_participants, read_item_table, promote_item_header, tidy_item_html, find_participant_table

@pytest.fixture
def temp_output_dir(tmp_path):
    return tmp_path

def test_process_items(temp_output_dir):
    fixture_path = Path("tests/fixtures/sample_item.html")
    
    # Create a temporary directory for the fixture to simulate the input_dir for process_items
    temp_fixture_dir = temp_output_dir / "raw_items"
    temp_fixture_dir.mkdir()
    (temp_fixture_dir / "sample_item.html").write_text(fixture_path.read_text())

    process_items(temp_fixture_dir, temp_output_dir)

    # Assert that the files exist and their content is as expected
    df_csv = pd.read_csv(temp_output_dir / "items.csv")
    assert len(df_csv) == 4
    assert "Male" in df_csv["Gender"].values
    assert (temp_output_dir / "items.feather").exists()
    assert (temp_output_dir / "items.parquet").exists()

def test_process_participants(temp_output_dir):
    fixture_path = Path("tests/fixtures/sample_participant.html")

    # Create a temporary directory for the fixture to simulate the input_dir for process_participants
    temp_fixture_dir = temp_output_dir / "raw_participants"
    temp_fixture_dir.mkdir()
    (temp_fixture_dir / "sample_participant.html").write_text(fixture_path.read_text())

    process_participants(temp_fixture_dir, temp_output_dir)

    # Assert that the files exist and their content is as expected
    df_csv = pd.read_csv(temp_output_dir / "participants.csv")
    assert len(df_csv) == 4 # 2 rows x 2 states
    assert "nsw" in df_csv["state"].values
    assert (temp_output_dir / "participants.feather").exists()
    assert (temp_output_dir / "participants.parquet").exists()