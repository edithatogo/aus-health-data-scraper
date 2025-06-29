
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
    output_csv = temp_output_dir / "items.csv"

    df_raw = read_item_table(fixture_path)

    if df_raw is not None:
        df_promoted = promote_item_header(df_raw)
        df_tidied = tidy_item_html(df_promoted)

        if df_tidied is not None and not df_tidied.empty:
            df_tidied.to_csv(output_csv, index=False)

    assert output_csv.exists()
    df = pd.read_csv(output_csv)
    assert len(df) == 4
    assert "Male" in df["Gender"].values

def test_process_participants(temp_output_dir):
    fixture_path = Path("tests/fixtures/sample_participant.html")
    output_csv = temp_output_dir / "participants.csv"

    html_content = fixture_path.read_text(encoding="utf-8")
    sio = io.StringIO(html_content)
    tables = pd.read_html(sio, flavor=["lxml", "bs4"])

    data_tbl = find_participant_table(tables, fixture_path.name)

    if data_tbl is not None:
        period = fixture_path.name.replace("sample_participant_", "").replace(".html", "")
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
        long.to_csv(output_csv, index=False)

    assert output_csv.exists()
    df = pd.read_csv(output_csv)
    assert len(df) == 4 # 2 rows x 2 states
    assert "nsw" in df["state"].values
