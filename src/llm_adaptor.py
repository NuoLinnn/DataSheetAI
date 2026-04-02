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




if __name__ == "__main__":
    get_all_table_schemas()