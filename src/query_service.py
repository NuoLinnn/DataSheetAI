import sqlite3
import os
import csv_loader
import schema_manager
import sql_validator

# Use cin from command line
def get_cli_command():
    while True:
        ask = input("What do you want to do: 'load CSV', 'run SQL query', or 'exit'? ")
        if ask.lower() == "load csv":
            filename = input("What is the filename? ")
            df = csv_loader.read_csv(filename)
            print("CSV successfully loaded. ")
            return df
        elif ask.lower() == "run sql query":
            query = input("Enter your SQL query: ")
            path = input("Enter your db path: ")
            print(f"Running query: {query}")
            result = run_sql_query(query, path)
            return result
        elif ask.lower() == "exit":
            print("Exiting... ")
            break
        else:
            print("That is not a valid statement. Please enter 'load CSV', 'run SQL query', or 'exit': ")

# Run a SQL Query
def run_sql_query(query_text, db_path):
    try:
        # Connect to the schema manager
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()

        # Then connect to SQL to run and return the result
        cur.execute(query_text)

        # Check if query is a select
        if sql_validator.query_type_validate(query_text) == True:
            results = cur.fetchall()
            print("The query was a success! Results: ")
            for row in results:
                print(row)

    # Check for database error
    except sqlite3.OperationalError as err:
        print("SQL error: ", err)

    except sqlite3.Error as err:
        print("Database error: ", err)

    # Once the query is done, close the connection
    finally:
        conn.close()


        





