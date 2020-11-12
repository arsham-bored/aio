import discord
from discord.ext import commands
from .controllers import (
    Booster,
    Bank
)
from .storage import UserBoostStorage
from .. import config
from ..orm import (
    get_all_boosts,
    get_all_transactions
)
from ..orm.engine import migrate
import logging

logging.basicConfig(level=logging.INFO)

count = 0

bot = commands.Bot(command_prefix='!AIO ')

booster = Booster(bot)
bank_controller = Bank(bot)

@bot.command(pass_context=True)
async def boost(ctx, *args):
    if booster.is_admin(ctx):
        await booster.send_message(ctx, *args)


@bot.command(pass_context=True)
async def clear(ctx, *args):
    UserBoostStorage.users = {}

@bot.command(pass_context=True)
async def bank(ctx, *args):
    await bank_controller.send_message(ctx)

@bot.command(pass_context=True)
async def dump(ctx, *args):
    boosts = "\n".join(
        f"price: {boost.price} - advertiser: {boost.advertiser.username} - key: {boost.key.username if boost.key is not None else 'none of them'}" for boost in get_all_boosts())
    ts = "\n".join(
        f"cut {t.price} for {t.user.username}" for t in get_all_transactions())

    await ctx.send(
        f"""
        **Boosts**
        {boosts}

        **Transactions**
        {ts}
        """
    )

if __name__ == "__main__":
    migrate()
    logging.info("bot started.")
    bot.run(config.token)
