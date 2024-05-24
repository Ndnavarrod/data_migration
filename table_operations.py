from mysql.connector import Error

def create_table(connection,create_table_query):
    """Create a new table in the database."""
    
    cursor = connection.cursor()
    try:
        cursor.execute(create_table_query)
        connection.commit()
        print("Table 'new_table' created successfully")
    except Error as e:
        print(f"Error: '{e}'")

def create_connection():
    """Create a database connection to a MySQL database."""
    connection = None
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="myuser",
            password="mypassword",
            database="mydatabase",
            port=3306
        )
        if connection.is_connected():
            print("Successfully connected to the database")
    except Error as e:
        print(f"Error: '{e}'")
    return connection