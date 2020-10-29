from ..engine import Base, session
from sqlalchemy import Column, Integer, String, Boolean
import logging


class User(Base):
    __tablename__ = "user"

    def __init__(self):
        super(User, self).__init__()

    id = Column(Integer, primary_key=True)
    username = Column(String)
    realm = Column(String)
    role = Column(String)

    is_raider = Column(Boolean)
    is_m = Column(Boolean)

    raider_link = Column(String)

    warcraft = Column(String)

    is_cloth = Column(Boolean)
    is_plate = Column(Boolean)
    is_leather = Column(Boolean)
    is_mail = Column(Boolean)

    referer = Column(String)
    info = Column(String)