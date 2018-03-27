import os

class Config():
    SECRET_KEY = os.urandom(24)
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://postgres:databasepass@localhost/weconnect"
