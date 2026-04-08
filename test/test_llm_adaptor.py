import pytest
from unittest.mock import patch, MagicMock
import llm_adaptor


# ── Fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture
def mock_conn():
    """Returns a mock database connection with a sample schema."""
    conn = MagicMock()
    cursor = MagicMock()
    cursor.fetchall.return_value = [("students", "CREATE TABLE students (id INTEGER PRIMARY KEY, name TEXT)")]
    conn.cursor.return_value = cursor
    return conn

@pytest.fixture
def mock_response():
    """Returns a mock Anthropic API response."""
    response = MagicMock()
    response.content = [MagicMock(text="```sql\nSELECT COUNT(*) FROM students;\n```")]
    return response


# ── get_all_table_schemas ─────────────────────────────────────────────────────

def test_get_all_table_schemas_returns_schemas(mock_conn):
    with patch("llm_adaptor.schema_manager.init", return_value=mock_conn):
        result = llm_adaptor.get_all_table_schemas()
        mock_conn.cursor().execute.assert_called_once()

def test_get_all_table_schemas_no_schemas(mock_conn):
    mock_conn.cursor().fetchall.return_value = []
    with patch("llm_adaptor.schema_manager.init", return_value=mock_conn):
        result = llm_adaptor.get_all_table_schemas()
        assert result is None  # function returns None implicitly when schemas is []


# ── get_claude_response ───────────────────────────────────────────────────────

def test_get_claude_response_returns_message(mock_conn, mock_response):
    with patch("llm_adaptor.schema_manager.init", return_value=mock_conn), \
         patch("llm_adaptor.anthropic.Anthropic") as mock_anthropic:

        mock_anthropic.return_value.messages.create.return_value = mock_response

        result = llm_adaptor.get_claude_response("how many students are there?")
        assert result == mock_response

def test_get_claude_response_calls_correct_model(mock_conn, mock_response):
    with patch("llm_adaptor.schema_manager.init", return_value=mock_conn), \
         patch("llm_adaptor.anthropic.Anthropic") as mock_anthropic:

        mock_anthropic.return_value.messages.create.return_value = mock_response
        llm_adaptor.get_claude_response("how many students are there?")

        call_kwargs = mock_anthropic.return_value.messages.create.call_args.kwargs
        assert call_kwargs["model"] == "claude-haiku-4-5-20251001"

def test_get_claude_response_includes_query_in_prompt(mock_conn, mock_response):
    with patch("llm_adaptor.schema_manager.init", return_value=mock_conn), \
         patch("llm_adaptor.anthropic.Anthropic") as mock_anthropic:

        mock_anthropic.return_value.messages.create.return_value = mock_response
        llm_adaptor.get_claude_response("how many students are there?")

        call_kwargs = mock_anthropic.return_value.messages.create.call_args.kwargs
        prompt = call_kwargs["messages"][0]["content"]
        assert "how many students are there?" in prompt


# ── extract_sql ───────────────────────────────────────────────────────────────

def test_extract_sql_valid():
    response = "```sql\nSELECT * FROM students;\n```"
    assert llm_adaptor.extract_sql(response) == "SELECT * FROM students;"

def test_extract_sql_no_sql_block():
    response = "Here is your answer: SELECT * FROM students;"
    assert llm_adaptor.extract_sql(response) == response

def test_extract_sql_multiline():
    response = "```sql\nSELECT name, major\nFROM students\nWHERE graduation_year = 2024;\n```"
    result = llm_adaptor.extract_sql(response)
    assert "SELECT name, major" in result
    assert "WHERE graduation_year = 2024;" in result

def test_extract_sql_strips_whitespace():
    response = "```sql\n  SELECT * FROM students;  \n```"
    assert llm_adaptor.extract_sql(response) == "SELECT * FROM students;"