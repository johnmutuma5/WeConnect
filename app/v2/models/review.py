from . import Base
from sqlalchemy import Column, Integer
from sqlalchemy.orm import relationship

class Review (Base):
    __tablename__ = 'review'
    # Table columns
    id = Column (Integer, primary_key=True)
    heading = Column ()
    body = Column ()
    author_id = Column ()
    business_id = Column ()


# class Review ():
#     '''
#     To create a review, use Review.create_review method to ensure propery fields are set
#     Review
#     Params: business_id, author_id, data
#     '''
#
#     review_index = 0
#
#     @classmethod
#     def create_review (cls, business_id, author_id, data):
#         cls.review_index = store.get_review_index ()
#         new_review = cls (business_id, author_id, data)
#         # assign to property fields
#         new_review.id = cls.review_index + 1
#         return new_review
#
#     @staticmethod
#     def gen_id_string (num):
#         return 'REV{:0>5}'.format(num)
#
#     def __init__ (self,business_id, author_id, data):
#         self.heading = data['heading']
#         self.body = data['body']
#         self.author_id = author_id
#         self.business_id = business_id
#         self._id = None
#
#     @property
#     def id (self):
#         return self._id
#
#     @id.setter
#     def id (self, id):
#         '''generates an 8-character commnet id e.g. REV00001
#         '''
#         self._id = 'REV{:0>5}'.format(id)
#         return
