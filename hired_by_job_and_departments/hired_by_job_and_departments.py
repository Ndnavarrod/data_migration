from flask import Flask, jsonify, render_template
import pandas as pd
from mysql.connector import Error
import mysql.connector
from tabulate import tabulate
import os
app = Flask(__name__)

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

@app.route('/api/data', methods=['GET'])
def get_data():
    connection = create_connection()
    if connection is None:
        return jsonify({"error": "Failed to connect to the database"}), 500

    sql = """
    SELECT 
        d.department, 
        j.job,  
        SUM(CASE WHEN QUARTER(h.datetime) = 1 THEN 1 ELSE 0 END) AS Q1, 
        SUM(CASE WHEN QUARTER(h.datetime) = 2 THEN 1 ELSE 0 END) AS Q2, 
        SUM(CASE WHEN QUARTER(h.datetime) = 3 THEN 1 ELSE 0 END) AS Q3,
        SUM(CASE WHEN QUARTER(h.datetime) = 4 THEN 1 ELSE 0 END) AS Q4  
    FROM 
        hired_employees h
    JOIN
        departments d ON h.department_id = d.id
    JOIN
        jobs j ON h.job_id = j.id
    WHERE 
        YEAR(h.datetime) = 2021 
    GROUP BY  
        d.department, 
        j.job
    ORDER BY
        d.department, 
        j.job
    """

    try:
        cursor = connection.cursor()
        cursor.execute(sql)
        records = cursor.fetchall()
        column_names = [desc[0] for desc in cursor.description]

        # Close the cursor and connection
        cursor.close()
        connection.close()

        # Convert records to a DataFrame and then to JSON
        df = pd.DataFrame(records, columns=column_names)
        result = df.to_dict(orient='records')

        return render_template('table.html', column_names=column_names, records=records)
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if connection.is_connected():
            connection.close()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
