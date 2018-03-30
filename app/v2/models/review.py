from . import Base
from sqlalchemy import Column, Sequence, ForeignKey, Integer, Text, String
from sqlalchemy.orm import relationship


class Review (Base):
    __tablename__ = 'review'
    # Table auto_increment sequence
    rev_id_seq = Sequence('rev_id_seq', start=1, metadata=Base.metadata)
    # Table columns
    id = Column('id', Integer, server_default=rev_id_seq.next_value(),
                primary_key=True)
    heading = Column(String(63), nullable=False)
    body = Column(Text, nullable=False)
    author_id = Column(Integer,
                       ForeignKey('users.id',
                                  ondelete='CASCADE',
                                  onupdate='CASCADE'), nullable=False)
    business_id = Column(Integer,
                         ForeignKey('business.id',
                                    ondelete='CASCADE',
                                    onupdate='CASCADE'), nullable=False)
    # relationships
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
