import pandas as pd
import mysql.connector

# Configuration parameters


def load_data_into_mysql(connection, table_name, csv_file, batch_size):
    # Read data from CSV file into a pandas DataFrame
    df = pd.read_csv(csv_file)

    # Establish connection to MySQL database
    
    # Create cursor
    cursor = connection.cursor()

    # Insert data into MySQL table in batches
    total_rows = len(df)
    num_batches = (total_rows // batch_size) + (1 if total_rows % batch_size != 0 else 0)

    for i in range(num_batches):
        start_idx = i * batch_size
        end_idx = min((i + 1) * batch_size, total_rows)

        batch_df = df.iloc[start_idx:end_idx]

        # Construct SQL query for batch insertion
        values = ", ".join(["(" + ", ".join([f"'{str(val)}'" for val in row]) + ")" for _, row in batch_df.iterrows()])
        sql = f"INSERT INTO {table_name} VALUES {values}"

        # Execute SQL query
        cursor.execute(sql)

    # Commit changes and close connection
    connection.commit()
    

    print(f"Data  Load successfully")
