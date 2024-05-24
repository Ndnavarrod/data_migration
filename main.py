import mysql.connector
from mysql.connector import Error
from table_operations import create_table
from table_operations import create_connection




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

def main():
    # Create a database connection
    connection = create_connection()
    
    if connection:
        # List all tables
        create_table_query = """
    CREATE TABLE IF NOT EXISTS employee_data (
        emp_id INT,
        first_name VARCHAR(100),
        last_name VARCHAR(100),
        birth_date DATE,
        hire_date DATE,
        salary DECIMAL(10, 2),
        department VARCHAR(100)
    ); """
        create_table(connection,create_table_query)
        list_tables(connection)

        # Close the connection
        if connection.is_connected():
            connection.close()
            print("The connection is closed")

if __name__ == "__main__":
    main()
