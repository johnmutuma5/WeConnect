from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Sequence
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property
from . import Base
from datetime import datetime, timedelta


class Token (Base):
    __tablename__ = 'token'

    # @staticmethod
    def compute_token_expiry ():
        return datetime.now()

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

    def __init__ (self, bearer_name, token_string):
        self.bearer_name = bearer_name
        self.token_string = token_string

    @hybrid_property
    def expired(self):
        ...
