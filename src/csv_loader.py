import pandas as pd
import sqlite3

#Read a CSV file using pandas
def read_csv (filename)
    #Use pandas.read_csv() to load data.
    df = pd.read_csv("test.csv")
    #If empty, print message saying database is empty and return
    if df.empty:
        print("Data frame is empty.")
        return
    else:
        return df
    

#Insert data into  SQLite.


#Run basic queries using sqlite3 or DB browser.
