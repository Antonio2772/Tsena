def connect_to_database(db_file):
    """Establish a connection to the Microsoft Access database."""
    import pyodbc
    connection_string = f"Driver={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={db_file};"
    connection = pyodbc.connect(connection_string)
    return connection

def execute_query(connection, query):
    """Execute a SQL query and return the results."""
    cursor = connection.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    return results

def format_data(cursor, data):
    """Format data for display in the GUI.
    
    Args:
        cursor: Database cursor containing the description of columns
        data: Query results to be formatted
        
    Returns:
        List of dictionaries mapping column names to their values
    """
    return [dict(zip([column[0] for column in cursor.description], row)) for row in data] if data else []