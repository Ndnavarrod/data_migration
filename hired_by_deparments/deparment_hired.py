from flask import Flask, jsonify
import pandas as pd
from mysql.connector import Error
import mysql.connector

app = Flask(__name__)

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
@app.route('/api/data2', methods=['GET'])
def get_hired_employees():
    connection = create_connection()
    if connection is None:
        return jsonify({"error": "Failed to connect to the database"}), 500

    sql = """
    SELECT 
        d.id,
        d.department, 
        COUNT(h.id) as hired
    FROM 
        hired_employees h
    JOIN
        departments d ON h.department_id=d.id
    WHERE 
        YEAR(h.datetime) = 2021 
    GROUP BY  
        d.department,
        d.id
    ORDER BY
        hired DESC 
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

        return jsonify(result)
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if connection.is_connected():
            connection.close()

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False)
