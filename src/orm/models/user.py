from typing import List
from ..engine import Base, session
from sqlalchemy import Column, Integer, String, Boolean, Integer
import logging


class User(Base):
    __tablename__ = "users"

    def __init__(self):
        super(User, self).__init__()

    id = Column('id', Integer, primary_key=True)

    category = Column('category', String)

    username = Column('username', String)
    realm = Column('realm', String)
    role = Column('role', String)

    is_raider = Column('is_raider', Boolean)
    is_m = Column('is_m', Boolean)

    raider_link = Column('raider_link', String)
    score = Column('score', Integer)

    warcraft = Column('warcraft', String)

    is_cloth = Column('is_cloth', Boolean)
    is_plate = Column('is_plate', Boolean)
    is_leather = Column('is_leather', Boolean)
    is_mail = Column('is_main', Boolean)

    referer = Column('referer', String)
    info = Column('info', String)

def get_user(username: str) -> List[User]:
    return session.query(User).filter(
        User.username == username
    ).all()