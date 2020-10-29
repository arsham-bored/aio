import discord
from .. import emojis
from .base import Controller
import logging

class Booster(Controller):

    def __init__(self, bot):
        self.__count = 0 #keep as reference
        self.bot = bot

    @property
    def count(self):
        self.__count += 1
        return self.__count

    @staticmethod
    def status(armor):
        return "yes" if armor == "yes" else "No Armor Stack"

    async def send_message(self, ctx, *args):
        try:
            name = ctx.author.name
            mention = ctx.author.mention

            armor, price, number_of_boost, realm, char = args

            coin = emojis.custome.get(self.bot, emojis.custome.coin)

            message = discord.Embed(title=f"{name} Boost", description=f"**Booster Cut:** {self.count} {coin}", color=0x28add1)
            message.add_field(name="Armor Stack", value=self.status(armor), inline=True)
            message.add_field(name="\t\t\tBoost Price", value=f"{price} {coin}", inline=True)
            message.add_field(name="\t\t\tNumber of Boost", value=str(number_of_boost), inline=True)
            message.add_field(name="Realm", value=str(realm), inline=True)
            message.add_field(name="\t\t\tChar to whisper", value=f"{char}-{realm}", inline=True)
            message.add_field(name="\t\t\tAdvertiser", value=mention, inline=True)

            post = await self.send_embed_message(ctx, message)

            await post.add_reaction(emojis.custome.get(self.bot, emojis.custome.shield))
            await post.add_reaction(emojis.custome.get(self.bot, emojis.custome.health))
            await post.add_reaction(emojis.custome.get(self.bot, emojis.custome.war))
            await post.add_reaction(emojis.custome.get(self.bot, emojis.custome.leader))

            
            def check(reaction, user):
                return user == ctx.author

            await self.bot.wait_for('reaction_add', check=check)
            await ctx.send("got reaction")

        except ValueError:
            await self.send_embed_message(ctx, discord.Embed(title="", description="please fill all fileds"))

        except Exception as error:
            logging.warning("not enough params to unpack")
            print(error)
            return