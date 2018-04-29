from ...exceptions import InvalidUserInputError
import re
from . import Base
from sqlalchemy import Column, Integer, String, Enum, Sequence, Index
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import func
from ...helpers import inspect_data


class User (Base):
    __tablename__ = 'users'
    # User id auto_increment sequence
    user_id_seq = Sequence('user_id_seq', start=1000, metadata=Base.metadata)
    # table columns
    id = Column('id', Integer, server_default=user_id_seq.next_value(),
                primary_key=True)
    _mobile = Column('mobile', String(12), nullable=False)
    _username = Column('username', String(63), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    first_name = Column(String(63), nullable=False)
    last_name = Column(String(63), nullable=False)
    gender = Column(Enum('Male', 'Female', name='gender_type'),
                    nullable=False)
    _email = Column('email', String(127), unique=True, nullable=False)
    # relationships
    businesses = relationship('Business', back_populates='owner')
    reviews = relationship('Review', back_populates='author')
    pass_reset_token = relationship(
        'Token', back_populates='bearer', uselist=False)


    # class variables
    required_fields = ['username', 'mobile', 'first_name',
        'last_name', 'gender', 'email', 'password']

    @classmethod
    def create_user(cls, data):
        # inspect_data raises a MissingDataError for blank fields
        cleaned_data = inspect_data(data, cls.required_fields)
        new_user = cls(cleaned_data)
        return new_user

    def __init__(self, data=None):
        if data:
            self.first_name = data['first_name']
            self.last_name = data['last_name']
            self.gender = data['gender']
            self.email = data['email']
            self.mobile = data['mobile']
            self.username = data['username']
            self.password = data['password']

    @hybrid_property
    def mobile(self):
        return self._mobile

    @mobile.setter
    def mobile(self, num):
        # should raise InvalidUserInputError with invalid chars in mobille numbers
        pattern = r"^[0-9]{12}$"
        match = re.match(pattern, num)
        if match:
            self._mobile = num
        else:
            raise InvalidUserInputError(
                "User::mobile.setter", "Invalid mobile number")

    @hybrid_property
    def username(self):
        return self._username

    @username.setter
    def username(self, name):
        pattern = r'^[a-zA-Z_]+[\d\w]{3,}'
        match = re.search(pattern, name)
        if match:
            self._username = name
            return
        self._username = None
        # assert 0, 'Invalid username'
        raise InvalidUserInputError("User::namesetter", "Invalid username!")

    @hybrid_property
    def email(self):
        return self._email

    @email.setter
    def email(self, email):
        email_pattern = r'^([\w\d_\.]+)@([\w\d]+)\.([\w\d]+\.?[\w\d]+)$'
        match = re.search(email_pattern, email)
        if match:
            self._email = email
            return
        raise InvalidUserInputError(msg='Invalid email')



Index('users_email_index', func.lower(User.email), unique=True)
Index('users_username_index', func.lower(User.username), unique=True)
