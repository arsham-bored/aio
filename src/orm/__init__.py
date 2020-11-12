from .engine import session
from .models.boost import Boost
from .models.transaction import Transaction

def get_all_boosts():
    return session.query(Boost).all()

def get_all_transactions():
    return session.query(Transaction).all()