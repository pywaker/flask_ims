"""
"""
from datetime import datetime

from .user import User, UserRole


USERS = {
    "admin": {
        "id": "admin",
        "email": "admin@example.net",
        "password": "SecretPassword",
        "role": UserRole.admin,
        "fullname": "Administrator",
        "is_active": True,
        "datetime": datetime.now()
    }
}

ITEMS = {}


def verify_user(email, password):
    for each in USERS.values():
        if each["email"] == email and each["password"] == password:
            return User(each)
    return None


def get_user_by_id(user_id):
    return User(USERS[user_id]) if user_id in USERS else None

def get_all_users():
    return USERS.values()

def get_all_items():
    print(ITEMS)
    return ITEMS.values()


def create_user(email, password, fullname):
    _id = email.lower()
    if _id in USERS:
        return False
    USERS[_id] = {
        "id": _id,
        "email": email,
        "password": password,
        "role": UserRole.staff,
        "fullname": fullname,
        "is_active": True,
        "datetime": datetime.now()
    }
    return True


def create_item(name, count=0):
    _id = "-".join(name.lower().split())
    if _id in ITEMS:
        return False
    ITEMS[_id] = {
        "id": _id,
        "name": name,
        "count": count
    }
    print(ITEMS)
    return True
