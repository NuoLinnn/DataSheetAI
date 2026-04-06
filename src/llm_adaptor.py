import anthropic
import os
import schema_manager

# hardcoded database path 
# TODO: migrate to query_service runner
db_path = "sample_data/datasheet.db"

def get_all_table_schemas():
    conn = schema_manager.init(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name, sql FROM sqlite_schema WHERE type='table' AND name NOT LIKE 'sqlite_%';")
    schemas = cursor.fetchall()

    if schemas is None:
        return "No schemas found"

    for table_name, schema_sql in schemas:
        print(f"Table: {table_name} Schema: {schema_sql}")
    conn.close()

def get_claude_response(user_query: str):
    table_schema = get_all_table_schemas()
    claude_prompt = (
        f"You are an AI assistant tasked with converting user queries into SQL statements. The database uses SQLite and contains the following tables: "
        f"{table_schema}"
        f"user query: {user_query}"
        f"Your task is to:"
        f"1. Generate a SQL query that accurately answers the user's question."
        f" 2. Ensure the SQL is compatible with SQLite syntax." 
        f"3. Provide a short comment explaining what the query does."
        f" Output Format: - SQL Query - Explanation"
        )
    
    client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    response = client.messages.create(
        model= "claude-haiku-4-5-20251001",
        max_tokens=1024,
        messages=[
            {"role":"user","content":claude_prompt}
        ]
    )

    print(claude_prompt)
    print(response)
    return response



if __name__ == "__main__":
    get_claude_response("tell me the number of students in the database")