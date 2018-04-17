import os


class Config():
    SECRET_KEY = os.urandom(24)


class ProductionConfig (Config):
    DEBUG = False
    TESTING = False
    PASSWORD_RESET_TOKEN_LIFETIME = {'hours':24}
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://postgres:databasepass@localhost/weconnect"


class DevelopmentConfig (Config):
    DEBUG = True
    TESTING = True
    PASSWORD_RESET_TOKEN_LIFETIME = {'seconds': 1}
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://postgres:databasepass@localhost/testdb"
