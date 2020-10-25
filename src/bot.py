import discord
from discord.ext import commands
from config import Config
from controllers import booster
import logging

logging.basicConfig(level=logging.INFO)

count = 0

bot = commands.Bot(command_prefix='!')

@bot.command(pass_context=True)
async def AIO(ctx, *args):
    await booster.send_message(ctx, *args)

if __name__ == "__main__":
    logging.info("bot started.")
    bot.run(Config().token)