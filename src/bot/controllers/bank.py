from typing import List
from ...orm.engine import session
from ...orm.models.transaction import Transaction
from ...orm.models.user import (
    User,
    get_user
)
from ..emojis import general
from ..utils import to_k
from datetime import datetime

class Bank:

    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    def week(t):
        return t.isocalendar()[1]

    @staticmethod
    def stringify(all_t: List[Transaction]):

        total = sum([t.price for t in all_t])
        return f"earned **{to_k(total)}**"

    @staticmethod
    def add_title(title, data):
        return f"**{title}**\n\n{data}\n"

    async def send_message(self, ctx, *args):
        user_registery = get_user(str(ctx.author)) 

        if len(user_registery) == 0:
            await  ctx.send(f"{ctx.author.mention} you are not registered")

        transactions = session.query(Transaction).filter(
            Transaction.user_id == user_registery[0].id
        )

        now = datetime.now()

        this_week = [t for t in transactions if self.week(t.time) == self.week(now)]
        last_week = [t for t in transactions if self.week(t.time) == self.week(now) - 1]

        this_week = self.add_title("This week", self.stringify(this_week))
        last_week = self.add_title("Last week", self.stringify(last_week))

        await ctx.author.send(f"{this_week}\n{last_week}")