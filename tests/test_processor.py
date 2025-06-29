
import pytest
from pathlib import Path
import pandas as pd
from src.processor import process_items, process_participants

@pytest.fixture
def temp_output_dir(tmp_path):
    return tmp_path

def test_process_items(temp_output_dir):
    fixture_path = Path("tests/fixtures")
    output_csv = temp_output_dir / "items.csv"
    process_items(fixture_path, output_csv)

    assert output_csv.exists()
    df = pd.read_csv(output_csv)
    assert len(df) == 2
    assert "Male" in df["Gender"].values

def test_process_participants(temp_output_dir):
    fixture_path = Path("tests/fixtures")
    output_csv = temp_output_dir / "participants.csv"
    process_participants(fixture_path, output_csv)

    assert output_csv.exists()
    df = pd.read_csv(output_csv)
    assert len(df) == 4 # 2 rows x 2 states
    assert "nsw" in df["state"].values
