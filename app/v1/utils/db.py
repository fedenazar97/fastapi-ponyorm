from pony.orm import Database, Required, Optional, Set
from app.v1.utils.settings import Settings

settings = Settings()

DB_PROVIDER = settings.db_provider
DB_NAME = settings.db_name
DB_USER = settings.db_user
DB_PASS = settings.db_pass
DB_HOST = settings.db_host


db = Database()

db.bind(provider=DB_PROVIDER, host = DB_HOST, user= DB_USER, passwd= DB_PASS, db= DB_NAME)

