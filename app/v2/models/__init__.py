from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from .user import User
from .business import Business
from .review import Review
from .token import Token


def init_db():
    from app.v2 import dbEngine
    Base.metadata.create_all(bind=dbEngine)

def drop_tables():
    from app.v2 import dbEngine
    Base.metadata.drop_all(bind=dbEngine)
