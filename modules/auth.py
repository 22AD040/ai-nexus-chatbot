import json
from pathlib import Path

USERS_FILE = Path("data/users.json")


def load_users():
    if not USERS_FILE.exists():
        USERS_FILE.parent.mkdir(exist_ok=True)
        USERS_FILE.write_text("{}")
    return json.loads(USERS_FILE.read_text())


def save_users(users):
    USERS_FILE.write_text(json.dumps(users, indent=2))


def register_user(fullname, email, password):
    users = load_users()
    email = email.lower()

    if email in users:
        return False, "User already exists"

    users[email] = {
        "fullname": fullname,
        "email": email,
        "password": password
    }

    save_users(users)
    return True, "Registered successfully"


def login_user(email, password):
    users = load_users()
    email = email.lower()

    user = users.get(email)

    if not user or user["password"] != password:
        return False, "Invalid credentials"

    return True, user