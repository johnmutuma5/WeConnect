import re
from datetime import date
from sqlalchemy.sql.expression import text, func
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from app.helpers import inspect_data
from sqlalchemy import(Column, Integer, String, Date, DateTime, Sequence,
                        ForeignKeyConstraint, Index, ForeignKey, Text)
from app.storage.base import Base
from app.exceptions import InvalidUserInputError, UnknownPropertyError
from .schemas import(REQUIRED_BUSINESS_FIELDS, VALID_BUSINESS_FIELDS,
                     USER_DEFINED_BUSINESS_FIELDS, REQUIRED_REVIEW_FIELDS,
                     VALID_REVIEW_FIELDS)


class Business (Base):
    __tablename__ = 'business'
    __table_args__ = (
        # we can use a FK at column level, constraint good for composite FKs
        ForeignKeyConstraint(['owner_id'], ['users.id'],
                             name='FK_business_user_id',
                             ondelete='CASCADE', onupdate='CASCADE'),
        Index('ix_business_name', text('LOWER(name)'), unique=True),
        {}
    )

    business_id_seq = Sequence(
        'business_id_seq',
        start=1000,
        metadata=Base.metadata)

    id = Column('id', Integer, server_default=business_id_seq.next_value(),
                primary_key=True)
    _mobile = Column('mobile', String(12), nullable=False)
    _name = Column('name', String(63), nullable=False, unique=True)
    owner_id = Column('owner_id', Integer, nullable=False)
    location = Column('location', String(127), nullable=False)
    category = Column("category", String(127), nullable=False)
    date_created = Column('date_created', DateTime, server_default=func.NOW(), nullable=False)
    # relationships
    owner = relationship('User', back_populates='businesses')
    reviews = relationship('Review', back_populates='business')

    # class variables
    required_fields = [*REQUIRED_BUSINESS_FIELDS]

    @classmethod
    def create_business(cls, data, owner_id):
        # inspect_data raises a MissingDataError for blank fields
        cleaned_data = inspect_data(data, cls.required_fields)
        new_business = cls(cleaned_data, owner_id)
        return new_business

    def __init__(self, data=None, owner_id=None):
        if data:
            self.mobile = data['mobile']
            self.name = data['name']
            self.location = data['location']
            self.category = data['category']
        self.owner_id = owner_id


    def profile(self):
        _profile = BusinessProfile(self)
        return _profile.generate()


    def update_profile(self, update_data):
        for key in update_data.keys():
            if key not in USER_DEFINED_BUSINESS_FIELDS:
                raise UnknownPropertyError(msg="Unknown property %s" %key)
            setattr(self, key, update_data[key])


    @hybrid_property
    def mobile(self):
        return self._mobile

    @hybrid_property
    def name(self):
        return self._name

    # property setters
    @mobile.setter
    def mobile(self, num):
        pattern = r"^[0-9]{12}$"
        match = re.match(pattern, num)
        if not match:
            raise InvalidUserInputError("Business::mobile.setter",
                                        "Invalid mobile number")
        self._mobile = num

    @name.setter
    def name(self, business_name):
        pattern = r'^([a-zA-Z]+( )?[\w\d_\.-]+( )?)+'
        match = re.match(pattern, business_name)
        if not match:
            raise InvalidUserInputError(msg='Invalid business name')
        self._name = business_name



class BusinessProfile(dict):
    def __init__(self, business):
        self.business = business

    def generate(self):
        fields = [*VALID_BUSINESS_FIELDS, "id"]
        for field in fields:
            value = getattr(self.business, field)
            if field in ('owner',):
                # extract owner name
                name = '{} {}'.format(value.first_name, value.last_name)
                value = {'name': name, 'id': value.id}
            # update dict key to value
            self[field] = value
        return self



class Review(Base):
    __tablename__ = 'review'
    __table_args__ = (
        Index('ix_review_publish_date',
              'author_id',
              'business_id',
              'publish_date',
              text('LOWER(heading)'),
              text('LOWER(body)'),
              unique=True), {}
    )

    rev_id_seq = Sequence('rev_id_seq', start=1000, metadata=Base.metadata)
    id = Column('id', Integer, server_default=rev_id_seq.next_value(),
                primary_key=True)
    heading = Column(String(63), nullable=False)
    body = Column(Text, nullable=False)
    author_id = Column(Integer, ForeignKey( 'users.id', ondelete='CASCADE',
                                            onupdate='CASCADE'),
                       nullable=False)
    business_id = Column(Integer, ForeignKey('business.id', ondelete='CASCADE',
                                             onupdate='CASCADE'),
                       nullable=False)
    publish_date = Column(Date, nullable=True, default=date.today())

    author = relationship('User', back_populates='reviews')
    business = relationship('Business', back_populates='reviews')

    @classmethod
    def create_review(cls, business_id, author_id, data):
        new_review = cls(business_id, author_id, data)
        return new_review

    def __init__(self, business_id, author_id, data):
        self.heading = data['heading']
        self.body = data['body']
        self.author_id = author_id
        self.business_id = business_id

    def to_dict(self):
        review_dict = ReviewDict(self)
        return review_dict.generate()


class ReviewDict(dict):
    def __init__(self, review):
        self.review = review

    def generate(self):
        fields = [*VALID_REVIEW_FIELDS, "id"]
        for field in fields:
            if field in ('author_id',):
                continue
            value = getattr(self.review, field)
            if field in ('author',):
                # extract owner name
                name = '{} {}'.format(value.first_name, value.last_name)
                value = {'name': name, 'id': value.id}

            self[field] = value
        return self
