from .. import store
from ...exceptions import InvalidUserInputError
import re
from . import Base
from sqlalchemy import Column, Integer, String, Enum, Sequence, ForeignKeyConstraint
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

class User (Base):
    __tablename__ = 'users'

    #table columns
    id = Column ('id', Integer, primary_key=True)
    _mobile = Column ('mobile', String(12), nullable=False)
    _username = Column ('username', String(64), nullable=False)
    password = Column (String(255), nullable=False)
    first_name = Column (String(63), nullable=False)
    last_name = Column (String(63), nullable=False)
    gender = Column (Enum('Male', 'Female'), nullable=False)
    _email = Column ('email', String(127), nullable=False)
    # relationships
    businesses = relationship ('Business', back_populates='owner')

    @classmethod
    def create_user (cls, data):
        cls.user_index = store.get_user_index ()
        new_user = cls (data)
        return new_user

    def __init__ (self, data=None):
        if data:
            self.first_name = data['first_name']
            self.last_name = data['last_name']
            self.gender = data['gender']
            self.email = data['email']
            self.mobile = data['mobile']
            self.username = data['username']
            self.password = data['password']

    @hybrid_property
    def mobile (self):
        return self._mobile

    @mobile.setter
    def mobile (self, num):
        # should raise InvalidUserInputError with invalid chars in mobille numbers
        pattern = r"^[0-9]{12}$"
        match = re.match (pattern, num)
        if match:
            self._mobile = num
        else:
            raise InvalidUserInputError ("User::mobile.setter", "Invalid mobile number")


    @hybrid_property
    def username (self):
        return self._username

    @username.setter
    def username (self, name):
        pattern = r'^[a-zA-Z_]+[\d\w]{3,}'
        match = re.search (pattern, name)
        if match:
            self._username = name
            return
        self._username = None
        # assert 0, 'Invalid username'
        raise InvalidUserInputError ("User::namesetter", "Invalid username!")

    @hybrid_property
    def email (self):
        return self._email

    @email.setter
    def email (self, email):
        # to do some format checks
        self._email = email
