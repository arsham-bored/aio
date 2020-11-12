from ..engine import Base, session
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    ForeignKey
)
from sqlalchemy.orm import relationship
from datetime import datetime
import logging


class Transaction(Base):

    __tablename__ = "transactions"

    def __init__(self):
        super(Transaction, self).__init__()

    id = Column('id', Integer, primary_key=True)
    price = Column(Integer)

    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", foreign_keys=[user_id])

    time = Column(DateTime, default=datetime.now)