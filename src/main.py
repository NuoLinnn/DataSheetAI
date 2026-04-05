import csv_loader
import schema_manager
import query_service
import sql_validator
import os

# test inputs
db_path = "sample_data/datasheet.db"
csv_file = "sample_data/students.csv"
table_name = os.path.splitext(os.path.basename(csv_file))[0]

# used to test functionality of code
def test():
    conn = schema_manager.init(db_path)
    
    # get table schema from input
    col_names, data_rows = csv_loader.read_csv(csv_file)

    # create table in sqlite
    schema_manager.create_table(conn, table_name, col_names)

    # insert data
    for row in data_rows:
        schema_manager.insert_into_table(conn, table_name, row)

    conn.commit()

    # get cli and run queries
    query_service.get_cli_command(col_names)
    
    #close connection
    conn.close()

if __name__ == "__main__":
    test()

