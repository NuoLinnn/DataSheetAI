# protect against database changes (delete, insert, set, etc)
## users
#   ensure results are valid
#   maek sure tables used are correct, and that columns are correct
import sqlite3
import os

# Only allow select queries
def query_type_validate(query_text):
    # Check if query is a select
    if query_text.strip().lower().startswith("select"):
        print("This is a select query")
        return True
    else:
        print("That is not a select query")
        return False

# Reject queries referencing unknown tables
def table_known(query_text, conn):
    in_query = query_text.lower().split()
    table_name = in_query[in_query.index("from") + 1]

    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [t[0] for t in cursor.fetchall()]

    if table_name not in tables:
        print(f"FAIL: The table {table_name} is not part of the database.")
        print("Available tables: ")
        for t in tables:
            print("-", t)
        return False
    else:
        print(f"PASS: The table {table_name} is part of the database.")
        return True

# Reject queries referencing unknown columns
def col_known(query_text, all_columns):
    in_query = query_text.lower().split()

    # Identify indices where there are columns (in the select statement)
    cols_start = in_query.index("select") + 1
    cols_end = in_query.index("from")

    selected_cols = " ".join(in_query[cols_start:cols_end]).split(",")
    selected_cols = [col.strip() for col in selected_cols]

    for col in selected_cols:
        if col != "*" and col not in all_columns:
            print(f"FAIL: The column {col} is not part of the database.")
            return False
        else:
            print(f"PASS: The column {col} is part of the database.")

    return True
