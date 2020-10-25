import discord
import emoji
import logging

class Booster:
    def __init__(self):
        self.__count = 0 #keep as reference

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

            message = discord.Embed(title=f"{name} Boost", description=f"**Booster Cut:** {self.count} <:coin:764530376202518539>", color=0x28add1)
            message.add_field(name="Armor Stack", value=self.status(armor), inline=True)
            message.add_field(name="\t\t\tBoost Price", value=f"{price} <:coin:764530376202518539>", inline=True)
            message.add_field(name="\t\t\tNumber of Boost", value=str(number_of_boost), inline=True)
            message.add_field(name="Realm", value=str(realm), inline=True)
            message.add_field(name="\t\t\tChar to whisper", value=f"{char}-{realm}", inline=True)
            message.add_field(name="\t\t\tAdvertiser", value=mention, inline=True)

            post = await self.send(ctx, message)

            await post.add_reaction()
            await post.add_reaction()
            await post.add_reaction()


        except Exception as error:
            logging.warning("not enough params to unpack")
            print(error)

            await self.send(ctx, discord.Embed(title="", description="not enough parameters"))
        
    @staticmethod
    async def send(ctx, embed):
        return await ctx.message.channel.send(embed=embed)