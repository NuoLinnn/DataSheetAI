# DataSheetAI
## System Overview
The system operates off of 5 modules: a CSV Loader, a Schema Manager, a Query Service, a SQL Validator, and an LLM adaptor. Each section is described briefly here:
### 1. CSV Loader
The CSV Loader is designed to load data and format it into a table for SQL Lite. It includes function read_csv(), which verifies if an input file is a CSV before reading it in and setting up a table schema. This function returns the column names and data rows of the dataframe that is read in. The next two functions, load_table_cols() and read_rows() return lists of the column headers and rows respectively. The last function, conn_sql(), takes a filename input and returns a SQLite connection so that basic queries can be run.
### 2. Schema Manager
### 3. Query Service
The query service allows for queries to be run interactively from the command line.
### 4. SQL Validator
### 5. LLM Adaptor

## How to Run Project
Run the project primarily from

## How to Run Tests
