import os


class Config():
    DEBUG = True
    TESTING = True
    SECRET_KEY = os.getenv('APP_SECRET')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL_TEST')
    NAMING_CONVENTION = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s"
    }
    NAMING_CONVENTION_REGEX = r"\"\w{2,}(_(?P<table>.+))?_(?P<column>.+)(_(?P<foreign_table>.+))?\""
    EMAIL_USERNAME = 'weconnect.mailer'
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
    EMAIL_PORT = 587

class ProductionConfig (Config):
    DEBUG = False
    TESTING = False
    PASSWORD_RESET_TOKEN_LIFETIME = {'hours':24}
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')


class DevelopmentConfig (Config):
    PASSWORD_RESET_TOKEN_LIFETIME = {'seconds': 1}


class TestingConfig(Config):
    PASSWORD_RESET_TOKEN_LIFETIME = {'seconds': 20}
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL_TEST')


env = {
    'dev': DevelopmentConfig,
    'prod': ProductionConfig,
    'test': TestingConfig # for postman: allows longer time for pass reset token expiry
}[os.getenv('ENVIRONMENT')]
