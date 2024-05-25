from flask import Flask, request, jsonify
from mysql.connector import Error
from table_operations import create_connection, init_databases
from load_data import load_data_into_mysql

app = Flask(__name__)

@app.route('/load_data', methods=['GET','POST'])
def load_data():
    # Get data from the request
    try:
        data = request.json
    except:
        return jsonify({'message': 'Missing args'})
    # Extract parameters from the request
    table_name = data.get('table_name')
    csv_file = data.get('csv_file')
    batch_size = data.get('batch_size')

    # Create a database connection
    connection = create_connection()
    
    try:
        # Initialize databases if not already initialized
        if connection.is_connected():
            init_databases(connection)

        # Load data into MySQL
        load_data_into_mysql(connection, table_name, csv_file, batch_size)

        return jsonify({'message': 'Data loaded successfully'})
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if connection.is_connected():
            connection.close()

if __name__ == "__main__":
    app.run(debug=False)
