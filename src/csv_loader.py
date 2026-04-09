import pandas as pd
import sqlite3
import os

#Read a CSV file using pandas
def read_csv (filename):
    # Check if the file type is a CSV
    if not filename.lower().endswith('.csv'):
        print("The file is not a CSV, cannot read it.")
        return None
    #Use pandas.read_csv() to load data.
    df = pd.read_csv(filename)
    #If empty, print message saying database is empty and return
    if df.empty:
        print("Data frame is empty.")
        return None

    # get the table col name and rows
    col_names = create_table_schema(df)
    data_rows = read_rows(df)

    return col_names, data_rows

# Create the column headers for SQL to use to create a table
def create_table_schema(df):
    # If the dataframe is empty return no columns
    if df is None:
        return []
    # If not return column headers
    col_names = df.columns.tolist()
    return col_names


def read_rows(df) -> list[list[str]]:
    if df is None:
        return []
    
    # add all rows from file and outputs them in a list
    return df.values.tolist()

# Connect to SQLite to run basic queries
def conn_sql(filename):
    try:
        conn = sqlite3.connect(filename)
        print("Successfully connected to SQLite")
        return conn 
    except sqlite3.Error as err:
        print(f"Error connecting to SQLite: {err}")
        return None




