from ...exceptions import InvalidUserInputError
import re
from . import Base
from sqlalchemy import Column, Integer, String, Sequence, ForeignKeyConstraint
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship


class Business (Base):
    __tablename__ = 'business'
    __table_args__ = (
        # we can use a FK at column level, constraint good for composite FKs
        ForeignKeyConstraint(['owner_id'], ['users.id'],
            name='FK_business_user_id',
            ondelete='CASCADE', onupdate='CASCADE'),
        {}
    )

    # tale auto_increment sequence
    business_id_seq = Sequence ('business_id_seq', start=1000,
                                    metadata=Base.metadata)
    # table columns
    _id = Column ('id', Integer, server_default=business_id_seq.next_value(),
                    primary_key=True)
    _mobile = Column ('mobile', String(12), nullable=False)
    name = Column ('name', String(63), nullable=False, unique=True)
    owner_id = Column ('owner_id', Integer, nullable=False)
    location = Column ('location', String(127), nullable=False)
    # relationships
    owner = relationship ('User', back_populates='businesses')
    reviews = relationship ('Review', back_populates='business')

    @classmethod
    def create_business (cls, data, owner_id):
        '''
            An alternative way of instantiating a business object
            directly with the class
        '''
        new_business = cls (data, owner_id)
        return new_business

    def __init__ (self, data=None, owner_id=None):
        if data:
            self.mobile = data['mobile']
            self.name = data['name']
            self.location = data ['location']
        self.owner_id = owner_id


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
            raise InvalidUserInputError ("Business::mobile.setter",
                                            "Invalid mobile number")
