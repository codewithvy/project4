import bcrypt

users = {}

def register_user(username, password):
    if username in users:
        return "User already exists!"
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    users[username] = hashed_password
    return "User registered successfully!"

def authenticate_user(username, password):
    if username not in users:
        return "User does not exist!"
    hashed_password = users[username]
    if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
        return "Login successful!"
    return "Invalid password!"
