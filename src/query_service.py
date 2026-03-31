import sqlite3
import os
import csv_loader

# Use cin from command line
def get_cli_command():
    while True:
        ask = input("What do you want to do: 'load CSV', 'run SQL query', or 'exit'?")
        if ask.lower()) == "load csv":
            filename = input("What is the filename?")
            df = read_csv(filename)
            print("CSV successfully loaded.")
            return df
        else if ask.lower() == "run sql query":
            query = input("Enter your SQL query:")
            print(f"Running query: {query}")
            result = run_sql_query(query)
        else if ask.lower() == "exit":
            print("Exiting...")
            break
        else
            print("That is not a valid statement. Please enter 'load CSV', 'run SQL query', or 'exit'")



def load_cs

