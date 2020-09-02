from pony.orm import Database, Required, Optional
from flask_login import UserMixin
from datetime import datetime


db = Database()
# db.bind(**DB_CONFIG)


class User(db.Entity, UserMixin):
    login = Required(str, unique=True)
    password = Required(str)
    last_login = Optional(datetime)


# db.generate_mapping(create_tables=True)
