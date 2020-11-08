import discord
from discord.ext import commands
from .controllers import Booster
from .storage import UserBoostStorage
from .. import config
from ..orm.engine import migrate
import logging

logging.basicConfig(level=logging.INFO)

count = 0

bot = commands.Bot(command_prefix='!AIO ')

booster = Booster(bot)

@bot.command(pass_context=True)
async def boost(ctx, *args):
    await booster.send_message(ctx, *args)

@bot.command(pass_context=True)
async def clear(ctx, *args):
    UserBoostStorage.users = {}

if __name__ == "__main__":
    migrate()
    logging.info("bot started.")
    bot.run(config.token)