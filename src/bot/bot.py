import discord
from discord.ext import commands
from config import Config
from controllers import Booster
import logging

logging.basicConfig(level=logging.INFO)

count = 0

bot = commands.Bot(command_prefix='!AIO ')

booster = Booster(bot)

@bot.command(pass_context=True)
async def boost(ctx, *args):
    await booster.send_message(ctx, *args)

if __name__ == "__main__":
    logging.info("bot started.")
    bot.run(Config().token)