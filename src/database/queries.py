def execute_query(connection, query):
    """Execute a SQL query and return the results."""
    cursor = connection.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    return results

def insert_data(connection, query, data):
    """Insert data into the database using a SQL query."""
    cursor = connection.cursor()
    cursor.execute(query, data)
    connection.commit()
    cursor.close()

def update_data(connection, query, data):
    """Update data in the database using a SQL query."""
    cursor = connection.cursor()
    cursor.execute(query, data)
    connection.commit()
    cursor.close()

def delete_data(connection, query):
    """Delete data from the database using a SQL query."""
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()
    cursor.close()