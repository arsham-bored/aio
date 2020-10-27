from engine import Base, session
from sqlalchemy import Column, Integer, String
import logging


class UserScore(Base):
    __tablename__ = "score"

    def __init__(self, user_id, chat_id):
        super(UserScore, self).__init__()

    id = Column(Integer, primary_key=True)
    username = Column(String)
    realm = Column(String)
    role = Column(String)

    


    def __repr__(self):
        return f"user: {self.user_id} from chat {self.chat_id} with score {self.score}"
