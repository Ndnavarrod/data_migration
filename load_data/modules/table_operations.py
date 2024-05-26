from mysql.connector import Error
import mysql.connector
import os
def create_table(connection,create_table_query):
    """Create a new table in the database."""
    
    cursor = connection.cursor()
    try:
        cursor.execute(create_table_query)
        connection.commit()
        print("Table created successfully")
    except Error as e:
        print(f"Error: '{e}'")

def create_connection():
    """Create a database connection to a MySQL database."""
    connection = None
    try:
        connection = mysql.connector.connect(
            host=os.getenv('MYSQL_HOST', 'localhost'),
            user=os.getenv('MYSQL_USER', 'myuser'),
            password=os.getenv('MYSQL_PASSWORD', 'mypassword'),
            database=os.getenv('MYSQL_DB', 'mydatabase'),
            port=3306
        )
        if connection.is_connected():
            print("Successfully connected to the database")
    except Error as e:
        print(f"Error: '{e}'")
    return connection
def list_tables(connection):
    """List all tables in the database."""
    cursor = connection.cursor()
    try:
        cursor.execute("SHOW TABLES;")
        tables = cursor.fetchall()
        print("Tables in the database:")
        for table in tables:
            print(table[0])
    except Error as e:
        print(f"Error: '{e}'")

def init_databases(connection):
     if connection:
        # List all tables
        create_hired_employees= """ CREATE TABLE IF NOT EXISTS hired_employees (   id INT,  name VARCHAR(100),   datetime DATETIME, department_id INT, job_id INT); """
        create_deparments= """ CREATE TABLE IF NOT EXISTS departments (   id INT,  department VARCHAR(100)); """
        create_jobs= """ CREATE TABLE IF NOT EXISTS jobs (   id INT,  job VARCHAR(100)); """
        create_table(connection,create_hired_employees)
        create_table(connection,create_deparments)
        create_table(connection,create_jobs)
        list_tables(connection)