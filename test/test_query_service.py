import pytest
from unittest.mock import patch, MagicMock
import sqlite3
import sys
sys.path.append('../src')
import query_service

# ── Fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture
def col_names():
    return ["name", "graduation_year", "major", "country_of_origin"]

@pytest.fixture
def mock_conn():
    conn = MagicMock(spec=sqlite3.Connection)
    cursor = MagicMock()
    cursor.fetchall.return_value = [("Alice", 2024, "CS", "USA")]
    conn.cursor.return_value = cursor
    return conn


# ── run_sql_query ─────────────────────────────────────────────────────────────

def test_run_sql_query_valid_select(mock_conn):
    with patch("query_service.sqlite3.connect", return_value=mock_conn), \
         patch("query_service.sql_validator.table_known", return_value=True), \
         patch("query_service.sql_validator.query_type_validate", return_value=True):

        result = query_service.run_sql_query("SELECT * FROM students", query_service.path)
        assert result == True

def test_run_sql_query_unknown_table(mock_conn):
    with patch("query_service.sqlite3.connect", return_value=mock_conn), \
         patch("query_service.sql_validator.table_known", return_value=False):

        result = query_service.run_sql_query("SELECT * FROM unknown_table", query_service.path)
        assert result == False

def test_run_sql_query_operational_error():
    mock_conn = MagicMock()
    mock_conn.cursor.return_value.execute.side_effect = sqlite3.OperationalError("no such table")

    with patch("query_service.sqlite3.connect", return_value=mock_conn), \
         patch("query_service.sql_validator.table_known", return_value=True), \
         patch("query_service.sql_validator.query_type_validate", return_value=True):

        result = query_service.run_sql_query("SELECT * FROM students", query_service.path)
        assert result == False

def test_run_sql_query_database_error():
    mock_conn = MagicMock()
    mock_conn.cursor.return_value.execute.side_effect = sqlite3.Error("generic db error")

    with patch("query_service.sqlite3.connect", return_value=mock_conn), \
         patch("query_service.sql_validator.table_known", return_value=True), \
         patch("query_service.sql_validator.query_type_validate", return_value=True):

        result = query_service.run_sql_query("SELECT * FROM students", query_service.path)
        assert result == False

def test_run_sql_query_closes_connection(mock_conn):
    with patch("query_service.sqlite3.connect", return_value=mock_conn), \
         patch("query_service.sql_validator.table_known", return_value=True), \
         patch("query_service.sql_validator.query_type_validate", return_value=True):

        query_service.run_sql_query("SELECT * FROM students", query_service.path)
        mock_conn.close.assert_called_once()

def test_run_sql_query_default_false_on_table_fail(mock_conn):
    """query_bool should be False when table_known returns False before query runs."""
    with patch("query_service.sqlite3.connect", return_value=mock_conn), \
         patch("query_service.sql_validator.table_known", return_value=False):

        result = query_service.run_sql_query("SELECT * FROM students", query_service.path)
        assert result == False


# ── get_cli_command: exit ─────────────────────────────────────────────────────

def test_cli_exit():
    with patch("builtins.input", return_value="exit"), \
         patch("builtins.print") as mock_print:

        query_service.get_cli_command()
        mock_print.assert_any_call("Exiting... ")

def test_cli_invalid_command():
    with patch("builtins.input", side_effect=["bad command", "exit"]), \
         patch("builtins.print") as mock_print:

        query_service.get_cli_command()
        mock_print.assert_any_call("That is not a valid statement. Please enter 'load CSV', 'run SQL query', 'print column names', or 'exit': ")


# ── get_cli_command: print column names ──────────────────────────────────────

def test_cli_print_column_names(col_names):
    with patch("builtins.input", side_effect=["print column names", "exit"]), \
         patch("builtins.print") as mock_print:

        query_service.get_cli_command(col_names)
        mock_print.assert_any_call(col_names)

def test_cli_print_column_names_none():
    """Should print None if no CSV has been loaded yet."""
    with patch("builtins.input", side_effect=["print column names", "exit"]), \
         patch("builtins.print") as mock_print:

        query_service.get_cli_command()
        mock_print.assert_any_call(None)


# ── get_cli_command: load csv ─────────────────────────────────────────────────

def test_cli_load_csv_success(col_names):
    with patch("builtins.input", side_effect=["load csv", "sample_data/test_students.csv", "exit"]), \
         patch("query_service.csv_loader.read_csv", return_value=(col_names, [["Alice", 2024, "CS", "USA"]])), \
         patch("builtins.print") as mock_print:

        query_service.get_cli_command()
        mock_print.assert_any_call("CSV successfully loaded. ")

def test_cli_load_csv_calls_read_csv():
    with patch("builtins.input", side_effect=["load csv", "sample_data/test_students.csv", "exit"]), \
         patch("query_service.csv_loader.read_csv", return_value=(["name"], [["Alice"]])) as mock_read, \
         patch("builtins.print"):

        query_service.get_cli_command()
        mock_read.assert_called_once_with("sample_data/test_students.csv")


# ── get_cli_command: run sql query ────────────────────────────────────────────

def test_cli_run_sql_query_success(col_names):
    query = "SELECT * FROM students"
    with patch("builtins.input", side_effect=["run sql query", query, "exit"]), \
         patch("query_service.sql_validator.query_type_validate", return_value=True), \
         patch("query_service.sql_validator.col_known", return_value=True), \
         patch("query_service.run_sql_query", return_value=True) as mock_run, \
         patch("builtins.print"):

        query_service.get_cli_command(col_names)
        mock_run.assert_called_once_with(query, query_service.path)

def test_cli_run_sql_query_invalid_type(col_names):
    """Should skip run_sql_query if query type validation fails."""
    query = "DROP TABLE students"
    with patch("builtins.input", side_effect=["run sql query", query, "exit"]), \
         patch("query_service.sql_validator.query_type_validate", return_value=False), \
         patch("query_service.run_sql_query") as mock_run, \
         patch("builtins.print"):

        query_service.get_cli_command(col_names)
        mock_run.assert_not_called()

def test_cli_run_sql_query_invalid_col(col_names):
    """Should skip run_sql_query if column validation fails."""
    query = "SELECT fake_col FROM students"
    with patch("builtins.input", side_effect=["run sql query", query, "exit"]), \
         patch("query_service.sql_validator.query_type_validate", return_value=True), \
         patch("query_service.sql_validator.col_known", return_value=False), \
         patch("query_service.run_sql_query") as mock_run, \
         patch("builtins.print"):

        query_service.get_cli_command(col_names)
        mock_run.assert_not_called()


# ── get_cli_command: ask claude ───────────────────────────────────────────────

def test_cli_ask_claude_calls_llm(col_names):
    mock_response = MagicMock()
    mock_response.content = [MagicMock(text="```sql\nSELECT COUNT(*) FROM students;\n```")]

    with patch("builtins.input", side_effect=["ask claude", "how many students?", "exit"]), \
         patch("query_service.llm_adaptor.get_claude_response", return_value=mock_response) as mock_llm, \
         patch("query_service.llm_adaptor.extract_sql", return_value="SELECT COUNT(*) FROM students;"), \
         patch("query_service.sql_validator.query_type_validate", return_value=True), \
         patch("query_service.sql_validator.col_known", return_value=True), \
         patch("query_service.run_sql_query", return_value=True), \
         patch("builtins.print"):

        query_service.get_cli_command(col_names)
        mock_llm.assert_called_once_with("how many students?")

def test_cli_ask_claude_invalid_query_type(col_names):
    """Should skip run_sql_query if Claude returns a non-SELECT query."""
    mock_response = MagicMock()
    mock_response.content = [MagicMock(text="```sql\nDROP TABLE students;\n```")]

    with patch("builtins.input", side_effect=["ask claude", "delete everything", "exit"]), \
         patch("query_service.llm_adaptor.get_claude_response", return_value=mock_response), \
         patch("query_service.llm_adaptor.extract_sql", return_value="DROP TABLE students;"), \
         patch("query_service.sql_validator.query_type_validate", return_value=False), \
         patch("query_service.run_sql_query") as mock_run, \
         patch("builtins.print"):

        query_service.get_cli_command(col_names)
        mock_run.assert_not_called()