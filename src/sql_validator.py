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
def table_known(query_text, table_name):
    words = query_text.lower().split()
    table_name = words[words.index("from") + 1]

    cursor = conn.cursor()


# Reject queries referencing unknown columns
def col_known(query_text, cols_name):
