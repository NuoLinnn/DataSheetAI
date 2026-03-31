import sqlite3
import os
import csv_loader

def init(db_path: str) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    print(f"Database created at: {os.path.abspath(db_path)}")
    return conn

def create_table_init_script(table_name: str, column_names:list[str]) -> str:
    """Sql script to create a table with given column names. PK will be autoincrement id"""

    columns = ["id INTEGER PRIMARY KEY AUTOINCREMENT"]
    for col in column_names:
        columns.append(f"{col} TEXT")

    joined_columns = ",\n            ".join(columns)
    sql = f""" CREATE TABLE IF NOT EXISTS {table_name} (
            {joined_columns}
    );"""
    return sql
    

def create_table(conn: sqlite3.Connection, table_name: str, column_names):
    """calls sqlite3 to create table with given table_name and column_names"""

    sql_script = create_table_init_script(table_name, column_names)

    with conn:
        conn.executescript(sql_script)
    
    print(f"Table {table_name} created successfully")


def create_insert_into_table_script(table_name: str, row: list[str]):
    """sql script to insert into table if it exists"""
    placeholders = ", ".join(["?" for _ in row])
    sql = f"INSERT INTO {table_name} VALUES (NULL, {placeholders})"
    return sql


def insert_into_table(conn: sqlite3.Connection, table_name: str, row: list[str]):
    """call sqlite to insert into table"""
    
    sql_script = create_insert_into_table_script(table_name, row)
    with conn:
        conn.execute(sql_script, row)