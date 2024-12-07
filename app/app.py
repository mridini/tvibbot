from flask import Flask, request, jsonify
import json
from datetime import datetime
import psycopg2

app = Flask(__name__)

# establish database connection
def get_db_connection():
    conn = psycopg2.connect(
        host="db", 
        database="tvibbot_db",
        user="tvibbot_user",
        password="tvibbot_password"
    )
    return conn

@app.route('/')
def home():
    time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return {
        "message": "Hello from Flask! I am currently running on a Docker Container!",
        "time": time
    }

@app.route('/webhook', methods=['POST'])
def webhook_listener():
    if request.is_json:
        data = request.get_json()
        print("Recieved data")
        print(data)

        # extract fields
        symbol = data.get('symbol')
        exchange = data.get('exchange', None) # optional
        price = data.get('price', None) 
        time = data.get('time', None)

        # connect to the db
        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            # insert
            cursor.execute("""
                INSERT INTO alerts (symbol, exchange, price, alert_time)
                VALUES (%s, %s, %s, %s);
            """, (symbol, exchange, price, time))
            # and commit
            conn.commit()
            return 'Data received and stored', 200
        except Exception as e:
            conn.rollback()
            return f"Error: {str(e)}", 500
        finally:
            cursor.close()
            conn.close()
    else:
        return "Invalid data", 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80) 
