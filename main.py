import mysql.connector
from mysql.connector import Error
from table_operations import create_connection, init_databases
from load_data import load_data_into_mysql

    
def main():
    # Create a database connection
    table_name="jobs"
    csv_file=r"C:\Users\Nelson\Documents\data_migration\inputs\jobs.csv"
    batch_size=1000
    connection = create_connection()
    cursor=connection.cursor()
    
    if connection.is_connected():
        init_databases(connection)
        load_data_into_mysql(connection, table_name, csv_file, batch_size)
        sql_query = "SELECT * FROM jobs;"
        cursor.execute(sql_query)
        rows = cursor.fetchall()
        for row in rows:
            print(row)

        connection.close()
        print("The connection is closed")

if __name__ == "__main__":
    main()
