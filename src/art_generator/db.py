import sqlite3

"""
Database for the MET tool. 
Supports the following functions:
1) Starts a connection to the database
2) Creates the database if it doesn't currently exist
3) Allows for creation, reading, update, and deletion of records
"""

def init_db(db_path):
    conn = sqlite3.connect(db_path)
    return conn