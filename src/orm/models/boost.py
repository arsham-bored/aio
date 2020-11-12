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
from sqlalchemy.orm import relationship
from datetime import datetime
import logging


class Boost(Base):
    __tablename__ = "boosts"

    def __init__(self):
        super(Boost, self).__init__()

    id = Column('id', Integer, primary_key=True)

    is_failed = Column(Boolean)
    price = Column(Integer)
    cut = Column(Integer)

    armor = Column(String)
    realm = Column(String)
    char = Column(String)
    required_key = Column(Integer)
    time = Column(DateTime, default=datetime.now)

    advertiser_id = Column(Integer, ForeignKey('users.id'))
    advertiser = relationship("User", foreign_keys=[advertiser_id])
    
    leader_id = Column(Integer, ForeignKey('users.id'))
    leader = relationship("User", foreign_keys=[leader_id])

    key_id = Column(Integer, ForeignKey('users.id'))
    key = relationship("User", foreign_keys=[key_id])

    healer_id = Column(Integer, ForeignKey('users.id'))
    healder = relationship("User", foreign_keys=[healer_id])

    tank_id = Column(Integer, ForeignKey('users.id'))
    tank = relationship("User", foreign_keys=[tank_id])

    dps_1_id = Column(Integer, ForeignKey('users.id'))
    dps_1 = relationship("User", foreign_keys=[dps_1_id])

    dps_2_id = Column(Integer, ForeignKey('users.id'))
    dps_2 = relationship("User", foreign_keys=[dps_2_id])
