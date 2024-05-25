import mysql.connector
from mysql.connector import Error
from table_operations import create_connection, init_databases
from load_data import load_data_into_mysql
import argparse
def parse_arguments():
    parser = argparse.ArgumentParser(description='Description of your program')
    
    # Define arguments with names and types
    parser.add_argument('--table_name', type=str, help='Description of argument 1')
    parser.add_argument('--csv_file', type=str, help='Description of argument 2')
    parser.add_argument('--batch_size', type=int, help='Description of argument 2')
    # Add more arguments as needed
    
    return parser.parse_args()
    
def main():
    args=parse_arguments()
    args.table_name

    # Create a database connection
    table_name=args.table_name
    csv_file=args.csv_file
    batch_size=args.batch_size
    print(table_name,csv_file,batch_size)
    connection = create_connection()
    cursor=connection.cursor()
    
    if connection.is_connected():
        init_databases(connection)
        load_data_into_mysql(connection, table_name, csv_file, batch_size)
        connection.close()
        print("The connection is closed")

if __name__ == "__main__":
    main()
