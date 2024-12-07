from flask import Flask, request, jsonify
from datetime import datetime
app = Flask(__name__)

@app.route('/')
def home():
    time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return {
        "message": "Hello from Flask! I am currently running on a Docker Container!",
        "time": time
    }


@app.route('/webhook', methods=['POST'])
def webhook_listener():
    data = request.get_json()
    
    if data:
        print("Received data:")
        print(data) 
        return jsonify({"message": "Data received successfully!"}), 200
    else:
        return jsonify({"error": "No data received"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80) 
