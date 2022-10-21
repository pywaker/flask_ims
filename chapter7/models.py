"""
"""
from datetime import datetime
from pony.orm import Database, Required, Optional, db_session, select
from flask_login import UserMixin

from .user import UserRole

db = Database()

class User(db.Entity, UserMixin):
    login = Required(str, unique=True)
    password = Required(str)
    role = Required(str)
    fullname = Optional(str)
    is_active = Required(bool)
    added_on = Required(datetime)
    last_login = Optional(datetime)


class Item(db.Entity):
    name = Required(str, unique=True)
    count = Required(int)
    added_on = Required(datetime)


def verify_user(email, password):
    user = User.get(login=email)
    return user if user.password == password else None


def get_all_users():
    return select(u for u in User).order_by(User.added_on)

def get_all_items():
    return select(i for i in Item).order_by(Item.added_on)


@db_session
def create_user(email, password, fullname, role=UserRole.staff):
    User(
        login=email,
        password=password,
        role=role.value,
        fullname=fullname,
        is_active=True,
        added_on=datetime.now()
    )


@db_session
def create_item(name, count=0):
    Item(name=name, count=count, added_on=datetime.now())


@db_session
def update_user_status(user_id, status):
    user = User.get(id=user_id)
    user.is_active = status
