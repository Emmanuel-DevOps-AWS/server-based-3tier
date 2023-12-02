import json
from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

# MySQL connection configuration
mysql_config = {
    'user': 'shar_admin',
    'password': 'adminadmin',
    'host': 'shar-db.cojtx1pbfoey.us-east-1.rds.amazonaws.com',
    'database': 'ShawarmaOrders',
}

@app.route('/place_order', methods=['POST'])
def place_order():
    try:
        data = request.json
        shawarma_type = data['shawarma_type']
        quantity = data['quantity']
        customer_name = data['customer_name']

        # Connect to MySQL
        conn = mysql.connector.connect(**mysql_config)
        cursor = conn.cursor()

        # Insert data into MySQL without specifying order_id (it will be auto-incremented)
        insert_query = "INSERT INTO ShawarmaOrders (shawarma_type, quantity, customer_name) VALUES (%s, %s, %s)"
        cursor.execute(insert_query, (shawarma_type, quantity, customer_name))

        # Commit changes and close connections
        conn.commit()
        cursor.close()
        conn.close()

        response_data = {
            "message": "Order placed successfully",
            "order_id": cursor.lastrowid  # Get the last auto-incremented ID
        }
        response = {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",  # This allows requests from any origin
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Methods": "OPTIONS,POST"  # Allow specified methods
        },
        "body": json.dumps(response_data)
        }

        return jsonify(response_data), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
