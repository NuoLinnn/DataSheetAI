import pytest
from unittest.mock import patch, MagicMock, call
import sqlite3
import os
import sys
sys.path.append('../src')
import schema_manager

# ── Fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture
def mock_conn():
    return MagicMock(spec=sqlite3.Connection)

@pytest.fixture
def col_names():
    return ["name", "graduation_year", "major", "country_of_origin"]

@pytest.fixture
def sample_row():
    return ["Alice", "2024", "CS", "USA"]


# ── init ──────────────────────────────────────────────────────────────────────

def test_init_returns_connection(tmp_path):
    db_path = str(tmp_path / "test.db")
    conn = schema_manager.init(db_path)
    assert isinstance(conn, sqlite3.Connection)
    conn.close()

def test_init_creates_db_file(tmp_path):
    db_path = str(tmp_path / "test.db")
    conn = schema_manager.init(db_path)
    assert os.path.exists(db_path)
    conn.close()

def test_init_prints_path(tmp_path, capsys):
    db_path = str(tmp_path / "test.db")
    conn = schema_manager.init(db_path)
    captured = capsys.readouterr()
    assert os.path.abspath(db_path) in captured.out
    conn.close()


# ── create_table_init_script ──────────────────────────────────────────────────

def test_create_table_init_script_contains_table_name(col_names):
    result = schema_manager.create_table_init_script("students", col_names)
    assert "students" in result

def test_create_table_init_script_has_primary_key(col_names):
    result = schema_manager.create_table_init_script("students", col_names)
    assert "id INTEGER PRIMARY KEY AUTOINCREMENT" in result

def test_create_table_init_script_has_all_columns(col_names):
    result = schema_manager.create_table_init_script("students", col_names)
    for col in col_names:
        assert col in result

def test_create_table_init_script_has_if_not_exists(col_names):
    result = schema_manager.create_table_init_script("students", col_names)
    assert "CREATE TABLE IF NOT EXISTS" in result

def test_create_table_init_script_columns_are_text(col_names):
    result = schema_manager.create_table_init_script("students", col_names)
    for col in col_names:
        assert f"{col} TEXT" in result

def test_create_table_init_script_empty_columns():
    result = schema_manager.create_table_init_script("students", [])
    assert "id INTEGER PRIMARY KEY AUTOINCREMENT" in result
    assert "students" in result


# ── create_table ──────────────────────────────────────────────────────────────

def test_create_table_calls_executescript(mock_conn, col_names):
    schema_manager.create_table(mock_conn, "students", col_names)
    mock_conn.executescript.assert_called_once()

def test_create_table_script_contains_table_name(mock_conn, col_names):
    schema_manager.create_table(mock_conn, "students", col_names)
    script = mock_conn.executescript.call_args[0][0]
    assert "students" in script

def test_create_table_prints_success(mock_conn, col_names, capsys):
    schema_manager.create_table(mock_conn, "students", col_names)
    captured = capsys.readouterr()
    assert "students" in captured.out
    assert "successfully" in captured.out


# ── create_insert_into_table_script ──────────────────────────────────────────

def test_create_insert_script_contains_table_name(sample_row):
    result = schema_manager.create_insert_into_table_script("students", sample_row)
    assert "students" in result

def test_create_insert_script_has_null_for_id(sample_row):
    result = schema_manager.create_insert_into_table_script("students", sample_row)
    assert "NULL" in result

def test_create_insert_script_correct_placeholder_count(sample_row):
    result = schema_manager.create_insert_into_table_script("students", sample_row)
    assert result.count("?") == len(sample_row)

def test_create_insert_script_single_row():
    result = schema_manager.create_insert_into_table_script("students", ["Alice"])
    assert result.count("?") == 1


# ── insert_into_table ─────────────────────────────────────────────────────────

def test_insert_into_table_calls_execute(mock_conn, sample_row):
    schema_manager.insert_into_table(mock_conn, "students", sample_row)
    mock_conn.execute.assert_called_once()

def test_insert_into_table_passes_row_as_params(mock_conn, sample_row):
    schema_manager.insert_into_table(mock_conn, "students", sample_row)
    _, call_args = mock_conn.execute.call_args
    # row is passed as second positional arg
    args = mock_conn.execute.call_args[0]
    assert args[1] == sample_row

def test_insert_into_table_uses_correct_table(mock_conn, sample_row):
    schema_manager.insert_into_table(mock_conn, "students", sample_row)
    sql = mock_conn.execute.call_args[0][0]
    assert "students" in sql

def test_insert_into_table_integration(tmp_path, col_names, sample_row):
    """Integration test using a real SQLite DB."""
    db_path = str(tmp_path / "test.db")
    conn = schema_manager.init(db_path)
    schema_manager.create_table(conn, "students", col_names)
    schema_manager.insert_into_table(conn, "students", sample_row)

    cur = conn.cursor()
    cur.execute("SELECT * FROM students")
    rows = cur.fetchall()
    assert len(rows) == 1
    assert rows[0][1] == "Alice"
    conn.close()