from ..engine import Base, session
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    ForeignKey
)
import logging


class Booster(Base):
    __tablename__ = "boosters"

    def __init__(self):
        super(User, self).__init__()

    id = Column('id', Integer, primary_key=True)
    advertiser = Column(Integer, ForeignKey('user.id'))
    is_failed = Column(Boolean)
    price = Column(Integer)

    armor = Column(String)
    realm = Column(String)
    char = Column(String)
    key = Column(Integer)
    time = Column(DateTime)

    healer = Column(Integer, ForeignKey('user.id'))
    tank = Column(Integer, ForeignKey('user.id'))
    dps = Column(Integer, ForeignKey('user.id'))