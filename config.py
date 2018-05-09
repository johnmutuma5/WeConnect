import os


class Config():
    DEBUG = True
    TESTING = True
    SECRET_KEY = 'asecretkeyfortheapi'
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://postgres:databasepass@localhost:5432/testdb"
    NAMING_CONVENTION = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s"
    }
    NAMING_CONVENTION_REGEX = r"\"\w{2,}(_(?P<table>.+))?_(?P<column>.+)(_(?P<foreign_table>.+))?\""


class ProductionConfig (Config):
    DEBUG = False
    TESTING = False
    PASSWORD_RESET_TOKEN_LIFETIME = {'hours':24}
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')


class DevelopmentConfig (Config):
    PASSWORD_RESET_TOKEN_LIFETIME = {'seconds': 1}


class TestingConfig(Config):
    PASSWORD_RESET_TOKEN_LIFETIME = {'seconds': 15}
