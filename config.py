import os

class Config():
    SECRET_KEY = os.urandom(24)
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://postgres:Mathematicss89@localhost/weconnect"
