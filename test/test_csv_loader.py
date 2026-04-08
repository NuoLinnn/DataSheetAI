import pytest
import pandas as pd
import os
import sys
sys.path.append('../src')
from csv_loader import read_csv, create_table_schema, read_rows


# ── Fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture
def sample_csv(tmp_path):
    """Creates a temporary valid CSV file for testing."""
    csv_content = "name,graduation_year,major,country_of_origin\nAlice,2024,CS,USA\nBob,2025,Math,Canada"
    file = tmp_path / "test.csv"
    file.write_text(csv_content)
    return str(file)

@pytest.fixture
def empty_csv(tmp_path):
    """Creates a temporary empty CSV file for testing."""
    file = tmp_path / "empty.csv"
    file.write_text("name,graduation_year,major,country_of_origin\n")
    return str(file)

@pytest.fixture
def sample_df():
    """Returns a sample pandas DataFrame for testing."""
    return pd.DataFrame({
        "name": ["Alice", "Bob"],
        "graduation_year": [2024, 2025],
        "major": ["CS", "Math"],
        "country_of_origin": ["USA", "Canada"]
    })

# ── read_csv ──────────────────────────────────────────────────────────────────

def test_read_csv_valid(sample_csv):
    result = read_csv(sample_csv)
    assert result is not None
    col_names, data_rows = result
    assert col_names == ["name", "graduation_year", "major", "country_of_origin"]
    assert len(data_rows) == 2

def test_read_csv_not_csv(tmp_path):
    txt_file = tmp_path / "test.txt"
    txt_file.write_text("some content")
    result = read_csv(str(txt_file))
    assert result is None

def test_read_csv_empty(empty_csv):
    result = read_csv(empty_csv)
    assert result is None

def test_read_csv_wrong_extension():
    result = read_csv("data.json")
    assert result is None

# ── create_table_schema ───────────────────────────────────────────────────────

def test_create_table_schema_valid(sample_df):
    result = create_table_schema(sample_df)
    assert result == ["name", "graduation_year", "major", "country_of_origin"]

def test_create_table_schema_none():
    result = create_table_schema(None)
    assert result == []

def test_create_table_schema_returns_list(sample_df):
    result = create_table_schema(sample_df)
    assert isinstance(result, list)

# ── read_rows ─────────────────────────────────────────────────────────────────

def test_read_rows_valid(sample_df):
    result = read_rows(sample_df)
    assert len(result) == 2
    assert result[0] == ["Alice", 2024, "CS", "USA"]
    assert result[1] == ["Bob", 2025, "Math", "Canada"]

def test_read_rows_none():
    result = read_rows(None)
    assert result == []

def test_read_rows_returns_list(sample_df):
    result = read_rows(sample_df)
    assert isinstance(result, list)
    assert all(isinstance(row, list) for row in result)