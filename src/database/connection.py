import pyodbc
import os

def create_connection(db_file):
    """Create a database connection to the Microsoft Access database specified by db_file."""
    conn = None
    try:
        # Normalize the path to handle slashes correctly
        db_path = os.path.normpath(db_file.strip('"'))
        
        # Create the connection string with proper formatting
        conn_str = (
            r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};"
            rf"DBQ={db_path};"
        )
        
        conn = pyodbc.connect(conn_str)
        print("Connection to database successful.")
        return conn
    except pyodbc.Error as e:
        print(f"Error: {e}")
        return None

def close_connection(conn):
    """Close the database connection."""
    if conn:
        conn.close()
        print("Connection closed.")