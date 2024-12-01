from flask import Flask, request, jsonify
from auth import register_user, authenticate_user

app = Flask(__name__)

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password are required!"}), 400

    message = register_user(username, password)
    return jsonify({"message": message})

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password are required!"}), 400

    message = authenticate_user(username, password)
    return jsonify({"message": message})

if __name__ == "__main__":
    app.run(debug=True)
