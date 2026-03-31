import sqlite3
import os

db_path = "datasheet.db"

def init(db_path: str) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    print(f"Database created at: {os.path.abspath(db_path)}")
