from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from .user import User
from .business import Business
from .review import Review
from .token import Token
