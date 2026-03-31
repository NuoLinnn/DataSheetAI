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
    else:
        return df
    

# Create the column headers for SQL to use to create a table
def create_table_schema(filename):
    # Use the read_csv function created above
    df = read_csv(filename)
    # If the dataframe is empty return no columns
    if df is None:
        return 0
    # If not return column headers
    col_names = df.columns.tolist()
    return col_names

# Check if data type is consistent for all rows
def validate_entries(filename):
    # Use the read_csv function created above
    df = read_csv(filename)
    # Go through data by rows and columns to validate that the type is correct
    for i in len(df.rows):
        for j in num_cols:
        
        # Figure out how to check column data type

    return print("The data types match")


