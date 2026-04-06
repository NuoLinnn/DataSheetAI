import sqlite3
import os
import csv_loader
import schema_manager
import sql_validator
import llm_adaptor

path = "sample_data/datasheet.db"

# Use cin from command line
def get_cli_command(col_names):
    while True:
        ask = input("What do you want to do: 'load CSV', 'run SQL query', 'ask Claude', 'print column names', or 'exit'? ")
        if ask.lower() == "load csv":
            filename = input("What is the filename? ")
            col_names, data_rows = csv_loader.read_csv(filename)
            print("CSV successfully loaded. ")

        elif ask.lower() == "run sql query":
            query = input("Enter your SQL query: ")
            # Validate the query type
            q_type_bool = sql_validator.query_type_validate(query)
            if q_type_bool == False:
                continue
            # Validate that the column(s) exist
            col_bool = sql_validator.col_known(query, col_names)
            if col_bool == False:
                continue

            print(f"Running query: {query}")
            result = run_sql_query(query, path)
            if result == False:
                continue
            return result

        elif ask.lower() == "ask claude":
            prompt = input("What would you like to know about your data?")
            print(f"Connecting to Claude and running query...")
            response = llm_adaptor.get_claude_response(prompt).content[0].text
            query = llm_adaptor.extract_sql(response)

            q_type_bool = sql_validator.query_type_validate(query)
            if q_type_bool == False:
                continue
            # Validate that the column(s) exist
            col_bool = sql_validator.col_known(query, col_names)
            if col_bool == False:
                continue

            print(f"Running query: {query}")
            result = run_sql_query(query, path)

        elif ask.lower() == "print column names":
            print(col_names)
            continue
            
        elif ask.lower() == "exit":
            print("Exiting... ")
            break
        else:
            print("That is not a valid statement. Please enter 'load CSV', 'run SQL query', 'print column names', or 'exit': ")

# Run a SQL Query
def run_sql_query(query_text, db_path):
    try:
        # Connect to the schema manager
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()

        # Validate that the table exist
        table_bool = sql_validator.table_known(query_text, conn)
        if table_bool == False:
            return table_bool

        # Then connect to SQL to run and return the result
        cur.execute(query_text)

        # Check if query is a select
        if sql_validator.query_type_validate(query_text) == True:
            results = cur.fetchall()
            print("The query was a success! Results: ")
            for row in results:
                print(row)
            query_bool = True
            

    # Check for database error
    except sqlite3.OperationalError as err:
        print("SQL error: ", err)
        query_bool = False

    except sqlite3.Error as err:
        print("Database error: ", err)
        query_bool = False

    # Once the query is done, close the connection
    finally:
        if 'conn' in locals():
            conn.close()

    return query_bool
