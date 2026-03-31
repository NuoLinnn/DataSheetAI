import csv_loader
import schema_manager
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

    for row in data_rows:
        schema_manager.insert_into_table(conn, table_name, row)
    #close connection
    conn.close()

if __name__ == "__main__":
    test()