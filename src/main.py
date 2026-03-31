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
    col_names = csv_loader.create_table_schema(csv_file)

    # create table in sqlite
    schema_manager.create_table(conn, table_name, col_names)

    schema_manager.insert_into_table(conn, table_name, ["Nuo Lin", "2027", "Computer Engeering" , "China"])
    #close connection
    conn.close()

if __name__ == "__main__":
    test()