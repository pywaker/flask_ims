"""
"""
from enum import Enum


class UserRole(Enum):
    admin = "Admin"
    staff = "Staff"
    guest = "Guest"


class User:
    def __init__(self, user):
        self._user = user

    @property
    def is_authenticated(self):
        return True
    
    @property
    def is_active(self):
        return self._user["is_active"]
    
    @property
    def is_anonymous(self):
        return False
    
    def get_id(self):
        return self._user["id"]
    
    @property
    def name(self):
        return self._user["fullname"]
