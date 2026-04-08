import pytest
from unittest.mock import MagicMock, patch
import sqlite3
import sys
sys.path.append('../src')
import sql_validator


# ── Fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture
def col_names():
    return ["name", "graduation_year", "major", "country_of_origin"]

@pytest.fixture
def mock_conn():
    conn = MagicMock(spec=sqlite3.Connection)
    cursor = MagicMock()
    cursor.fetchall.return_value = [("students",)]
    conn.cursor.return_value = cursor
    return conn


# ── query_type_validate ───────────────────────────────────────────────────────

def test_query_type_validate_select():
    assert sql_validator.query_type_validate("SELECT * FROM students") == True

def test_query_type_validate_select_lowercase():
    assert sql_validator.query_type_validate("select * from students") == True

def test_query_type_validate_select_leading_whitespace():
    assert sql_validator.query_type_validate("   SELECT * FROM students") == True

def test_query_type_validate_drop():
    assert sql_validator.query_type_validate("DROP TABLE students") == False

def test_query_type_validate_delete():
    assert sql_validator.query_type_validate("DELETE FROM students") == False

def test_query_type_validate_insert():
    assert sql_validator.query_type_validate("INSERT INTO students VALUES (1)") == False

def test_query_type_validate_update():
    assert sql_validator.query_type_validate("UPDATE students SET name='Bob'") == False


# ── table_known ───────────────────────────────────────────────────────────────

def test_table_known_valid(mock_conn):
    result = sql_validator.table_known("SELECT * FROM students", mock_conn)
    assert result == True

def test_table_known_invalid(mock_conn):
    result = sql_validator.table_known("SELECT * FROM unknown_table", mock_conn)
    assert result == False

def test_table_known_missing_from(mock_conn):
    result = sql_validator.table_known("SELECT * students", mock_conn)
    assert result is None

def test_table_known_strips_semicolon(mock_conn):
    result = sql_validator.table_known("SELECT * FROM students;", mock_conn)
    assert result == True

def test_table_known_case_insensitive_from(mock_conn):
    result = sql_validator.table_known("SELECT * FROM students", mock_conn)
    assert result == True

def test_table_known_prints_available_tables_on_fail(mock_conn, capsys):
    sql_validator.table_known("SELECT * FROM unknown_table", mock_conn)
    captured = capsys.readouterr()
    assert "students" in captured.out

def test_table_known_queries_sqlite_master(mock_conn):
    sql_validator.table_known("SELECT * FROM students", mock_conn)
    mock_conn.cursor().execute.assert_called_with("SELECT name FROM sqlite_master WHERE type='table'")


# ── col_known ─────────────────────────────────────────────────────────────────

def test_col_known_valid(col_names):
    result = sql_validator.col_known("SELECT name FROM students", col_names)
    assert result == True

def test_col_known_wildcard(col_names):
    result = sql_validator.col_known("SELECT * FROM students", col_names)
    assert result == True

def test_col_known_invalid_col(col_names):
    result = sql_validator.col_known("SELECT fake_col FROM students", col_names)
    assert result == False

def test_col_known_multiple_valid_cols(col_names):
    result = sql_validator.col_known("SELECT name, major FROM students", col_names)
    assert result == True

def test_col_known_one_invalid_in_multiple(col_names):
    result = sql_validator.col_known("SELECT name, fake_col FROM students", col_names)
    assert result == False

def test_col_known_aggregate_count_wildcard(col_names):
    result = sql_validator.col_known("SELECT COUNT(*) FROM students", col_names)
    assert result == True

def test_col_known_aggregate_count_column(col_names):
    result = sql_validator.col_known("SELECT COUNT(name) FROM students", col_names)
    assert result == True

def test_col_known_aggregate_sum(col_names):
    result = sql_validator.col_known("SELECT SUM(graduation_year) FROM students", col_names)
    assert result == True

def test_col_known_aggregate_invalid_column(col_names):
    result = sql_validator.col_known("SELECT COUNT(fake_col) FROM students", col_names)
    assert result == False

def test_col_known_case_insensitive(col_names):
    result = sql_validator.col_known("select NAME from students", col_names)
    assert result == True