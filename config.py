import os


class Config():
    DEBUG = True
    TESTING = True
    SECRET_KEY = 'asecretkeyfortheapi'
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://postgres:databasepass@localhost:5432/testdb"


class ProductionConfig (Config):
    DEBUG = False
    TESTING = False
    PASSWORD_RESET_TOKEN_LIFETIME = {'hours':24}
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')


class DevelopmentConfig (Config):
    PASSWORD_RESET_TOKEN_LIFETIME = {'seconds': 1}


class TestingConfig(Config):
    PASSWORD_RESET_TOKEN_LIFETIME = {'seconds': 15}
