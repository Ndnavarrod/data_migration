import pandas as pd
import mysql.connector

# Configuration parameters

def read_jobs(csv_file):
    columns_names=['id','job']
    
    dtype_dict = {
        'id': 'int',
        'job': 'str'  
    }
    df = pd.read_csv(csv_file, header=None, names=columns_names, dtype=dtype_dict)
    df=df.dropna()
    return df
def read_deparments(csv_file):
    columns_names=['id','department']
    
    dtype_dict = {
        'id': 'int',
        'department': 'str'  
    }
    df = pd.read_csv(csv_file, header=None, names=columns_names, dtype=dtype_dict)
    df=df.dropna()
    return df
def read_hired_employees(csv_file):
    columns_names=['id','name','datetime','deparment_id','job_id']
    
  
    df = pd.read_csv(csv_file, header=None, names=columns_names)
    df=df.dropna()
    df['datetime'] = pd.to_datetime(df['datetime'])
    df['datetime'] = df['datetime'].dt.tz_convert(None)
    df.loc[df['name'].str.contains("'"), 'name'] = ""
    return df
def load_data_into_mysql(connection, table_name, csv_file, batch_size):
    
    if table_name=="jobs":
        df=read_jobs(csv_file)
    elif table_name=="departments":
        df=read_deparments(csv_file)
    elif table_name=="hired_employees":
        df=read_hired_employees(csv_file)
    else:
        print("Invalid table name")
        df=pd.DataFrame()
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
