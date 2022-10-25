from pony.orm import Database, Required, Optional, Set

from app.v1.utils.db import db

class User(db.Entity):
    username = Required(str, unique = True)
    password = Required(str)
    mail = Required(str, unique = True)