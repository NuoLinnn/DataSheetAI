# DataSheetAI
## System Overview
The system operates off of 5 modules: a CSV Loader, a Schema Manager, a Query Service, a SQL Validator, and an LLM adaptor. Each section is described briefly here:
### 1. CSV Loader
The CSV Loader is designed to load data and format it into a table for SQL Lite. It includes function read_csv(), which verifies if an input file is a CSV before reading it in and setting up a table schema. This function returns the column names and data rows of the dataframe that is read in. The next two functions, create_table_schema() and read_rows() return lists of the column headers and rows respectively. The last function, conn_sql(), takes a filename input and returns a SQLite connection so that basic queries can be run.
### 2. Schema Manager
The schema manager starts with an init() function that opens a connection to SQLite and creates a database at a given path. The function create_table_init_script() creates a table with given column names and a primary key that auto-increments. Then, create_table() calls that script and connects to SQLite to execute it. Several additional functions were made to include other options. The function create_insert_into_table_script() will insert into a table if the table exists. Then the function insert_into_table() connects to SQLite to execute create_insert_into_table_script().
### 3. Query Service
The query service allows for queries to be run interactively from the command line using the get_cli_command(). There are several options here, including: load CSV, run SQL query, ask Claude, print column names, or exit. No matter what you enter on the command line prompt, the system will give you a response, and if your entry does not return a result the system will give feedback to improve your entry. This function also calls internally on the other function in this module, run_sql_query(), which connects to SQLite to validate your table name exists, validate that you are running a SELECT query, and run the query. The module will also validate that the column names exist in the command line interface function. If there are errors in SQLite, those are returned in the command line for the user to see.
### 4. SQL Validator
The SQL validator performs several functions. The first is query_type_validate(), which checks whether a query is a select query and rejects it if the query is not. The next function the validator performs is table_known(), which checks whether a table that is called in a query is part of the database. If it is not, the function prints all of the available table names to be called. The final function, col_known(), checks whether a column is part of the table that is called. If it is not, the query will fail.
### 5. LLM Adaptor
The LLM adaptor interfaces with an LLM to create a query that takes a general user input and is compatible with SQLite. The first function it uses is get_all_table_schemas(), which will print all the table names and schemas if any exist. The next function, get_claude_response() interfaces with the LLM by feeding it a prompt and returning a response. Finally, the function extract_sql() takes only the SQL response from the LLM, ignoring any other text.
## How to Run Project


## How to Run Tests
The unit tests create a sample data file and 

The main.py file also created a streamlined location to test individual functions within modules and allow them to interface with each other.
