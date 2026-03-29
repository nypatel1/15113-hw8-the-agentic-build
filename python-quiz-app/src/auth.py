import json
import hashlib
import os

USERS_FILE = 'data/users.json'

def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, 'r') as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register(username, password):
    users = load_users()
    if username in users:
        return False  # User already exists
    users[username] = hash_password(password)
    save_users(users)
    return True

def login(username, password):
    users = load_users()
    if username in users and users[username] == hash_password(password):
        return True
    return False