import re
from datetime import datetime, timedelta
from app import config
from app.storage.base import Base
from app.user.schemas import USER_DEFINED_USER_FIELDS, VALID_USER_FIELDS
from app.exceptions import InvalidUserInputError
from app.helpers import inspect_data, hash_password

from sqlalchemy import Column, Integer, String, Enum, Sequence, Index, DateTime, ForeignKey
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text


class User(Base):
    __tablename__ = 'users'
    __table_args__ = (
        Index('ix_user_email', text('LOWER(users.email)'), unique=True),
        Index('ix_user_username', text('LOWER(users.username)'), unique=True)
    )

    user_id_seq = Sequence('user_id_seq', start=1000, metadata=Base.metadata)
    # table columns
    id = Column('id', Integer, server_default=user_id_seq.next_value(),
                primary_key=True)
    _mobile = Column('mobile', String(12), nullable=False)
    _username = Column('username', String(63), unique=True, nullable=False)
    _password = Column("password", String(255), nullable=False)
    first_name = Column(String(63), nullable=False)
    last_name = Column(String(63), nullable=False)
    gender = Column(Enum('Male', 'Female', name='gender_type'),
                    nullable=False)
    _email = Column('email', String(127), unique=True, nullable=False)
    # relationships
    businesses = relationship('Business', back_populates='owner')
    reviews = relationship('Review', back_populates='author')
    pass_reset_token = relationship(
        'PasswordResetToken', back_populates='bearer', uselist=False)

    # class variables
    writable_fields = [*USER_DEFINED_USER_FIELDS]

    @classmethod
    def create_user(cls, data):
        # inspect_data raises a MissingDataError for blank fields
        cleaned_data = inspect_data(data, cls.writable_fields)
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

    def profile(self, profile_type=None):
        profile = PrivateUserProfile(self)
        return profile.get_dict()

    # use hybrid_property to make the property accessible with sqlalchemy
    # filter
    @hybrid_property
    def mobile(self):
        return self._mobile

    @hybrid_property
    def username(self):
        return self._username

    @hybrid_property
    def email(self):
        return self._email

    @hybrid_property
    def password(self):
        passhash = self._password
        return passhash

    # property setters
    @mobile.setter
    def mobile(self, num):
        # should raise InvalidUserInputError with invalid chars in mobile
        # numbers
        pattern = r"^[0-9]{12}$"
        match = re.match(pattern, num)
        if match:
            self._mobile = num
        else:
            raise InvalidUserInputError(
                "User::mobile.setter", "Invalid mobile number")

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

    @email.setter
    def email(self, email):
        email_pattern = r'^([\w\d_\.]+)@([\w\d]+)\.([\w\d]+\.?[\w\d]+)$'
        match = re.search(email_pattern, email)
        if match:
            self._email = email
            return
        raise InvalidUserInputError(msg='Invalid email')

    @password.setter
    def password(self, password):
        passhash = hash_password(password)
        self._password = passhash



class UserProfile():
    def __init__(self, user):
        self.user = user

    def _process_business_list(self, business_list):
        func = lambda business: {
            'id': business.id,
            'name': business.name
        }
        businesses_map = map(func, business_list)
        value = list(businesses_map)
        return value

    def _process_reviews_list(self, reviews_list):
        func = lambda review: {
            'id': review.id,
            'heading': review.heading
        }
        reviews_map = map(func, reviews_list)
        value = list(reviews_map)
        return value


class PrivateUserProfile(UserProfile):
    def get_dict(self):
        user_profile = {}
        for attribute in VALID_USER_FIELDS:
            value = getattr(self.user, attribute)
            if attribute in ('businesses',):
                value = self._process_business_list(value)

            if attribute in ('reviews'):
                value = self._process_reviews_list(value)

            user_profile[attribute] = value

        return user_profile



def compute_token_expiry():
    token_lifetime = config['PASSWORD_RESET_TOKEN_LIFETIME']
    # unpack token_lifetime dict into time_delta
    return datetime.now() + timedelta(**token_lifetime)


class PasswordResetToken (Base):
    __tablename__ = 'token'

    token_id_seq = Sequence('token_id_seq', metadata=Base.metadata, start=1)
    id = Column(Integer, primary_key=True,
                server_default=token_id_seq.next_value())
    bearer_name = Column(String(63),
                         ForeignKey('users.username',
                                    ondelete='CASCADE',
                                    onupdate='CASCADE'),
                         nullable=False,
                         unique=True)
    token_string = Column(String(98), nullable=False, unique=True)
    expires_at = Column(DateTime, default=compute_token_expiry, nullable=False)

    bearer = relationship('User', back_populates='pass_reset_token')

    def __init__(self, token_string, bearer_name):
        self.bearer_name = bearer_name
        self.token_string = token_string

    @hybrid_property
    def expired(self):
        expires_at = str(self.expires_at)
        expiry_time = datetime.strptime(expires_at, '%Y-%m-%d %H:%M:%S.%f')
        now = datetime.now(tz=None)
        return now > expiry_time
