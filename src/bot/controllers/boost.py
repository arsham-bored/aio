import discord
from discord import Color
from discord.ext import tasks
from datetime import datetime
import asyncio
from ...orm.engine import session
from ...orm.models.user import User
from .. import emojis
from ..storage import BoosterStorage
from .base import Controller
import logging
import uuid


class Booster(Controller):

    def __init__(self, bot):
        self.__count = 0  # keep as reference
        self.bot = bot

        # controll icons
        self.trigger = emojis.general.hammer
        self.cancel = emojis.general.cancel
        self.lock = emojis.general.lock
        self.voice = emojis.general.voice

    class Message:
        def __init__(self, ctx, storage=None, boosters=None):
            self.ctx = ctx
            self.boosters = boosters
            self.storage = storage

    class BoostItems:
        def __init__(self, helmet, health, war):
            self.items = [helmet, health, war]

        def __contains__(self, icon):
            return icon in self.items

    class Timer:

        @staticmethod
        def get_difference(time: datetime):
            now = datetime.now()
            difference = now - time
            return difference.total_seconds()

    class Memory:
        def __init__(self):
            self.channel = None
            self.role = None
            self.triggered = False
            self.now = datetime.now()
            self.timer_stop = False
            self.first_time = True

    @staticmethod
    def status(armor: str):
        if armor.startswith("y"):
            _, case = armor.split(":")

            if case == "c":
                return "yes : **Cloth**"

            elif case == "l":
                return "yes : **Leather**"

            elif case == "p":
                return "yes : **Plate**"

            elif case == "m":
                return "yes : **Mail**"

            else:
                return "yes"

        return "no"


    @staticmethod
    def calculate_cut(price: int):
        percent = 32 / 100
        x = percent * price
        x = price - x
        return int(x / 4)

    async def generate_message(self, data: Message, *args) -> discord.Embed:

        print("update boost message")

        ctx = data.ctx
        name = ctx.author.name
        mention = ctx.author.mention

        if len(args) == 6:
            name, armor, price, number_of_boost, realm, char = args
            key = ""

        elif len(args) == 7:
            key, name, armor, price, number_of_boost, realm, char = args

            key_score = int(key.replace("+", ""))
            if key_score > 35:
                await data.ctx.send("specific key is way more than maximum")

        else:
            await data.ctx.send("double check your command")

        self.coin = emojis.custome.coin.to_unicode(self.bot)
        self.helmet = emojis.custome.helmet.to_unicode(self.bot)
        self.health = emojis.custome.health.to_unicode(self.bot)
        self.war = emojis.custome.war.to_unicode(self.bot)
        self.brand = emojis.custome.brand.to_unicode(self.bot)
        self.key = emojis.custome.key.to_unicode(self.bot)
        self.leader = emojis.custome.leader.to_unicode(self.bot)

        self.helmet_cross = emojis.custome.helmet_cross.to_unicode(self.bot)
        self.health_cross = emojis.custome.health_cross.to_unicode(self.bot)
        self.war_cross = emojis.custome.war_cross.to_unicode(self.bot)
        self.war_double_cross = emojis.custome.war_double_cross.to_unicode(
            self.bot)

        self.boost_items = self.BoostItems(self.helmet, self.health, self.war)

        message = discord.Embed(title=f"{ctx.author.name}'s Boost",
                                description=f"**{key}{' - ' if key != '' else ''} {name.upper()}**", color=Color.orange())
        message.add_field(
            name=f"\u200b", value=f"**Boost Cut:** {self.calculate_cut(int(price))} {self.coin}", inline=False)
        message.add_field(name="Armor Stack\t\t\t\t\t  ",
                          value=self.status(armor), inline=True)
        message.add_field(name="Boost Price\t\t\t\t\t  ",
                          value=f"{price} {self.coin}", inline=True)
        message.add_field(name="Number of Boost",
                          value=str(number_of_boost), inline=True)
        message.add_field(name="Realm\t\t\t\t\t  ",
                          value=str(realm).capitalize(), inline=True)
        message.add_field(name="Char to whisper\t\t\t\t\t  ",
                          value=f"{char}-{realm}", inline=True)
        message.add_field(name="Specific key\t\t\t\t\t  ",
                          value=f"`{key}`", inline=True)
        message.add_field(name="Advertiser", value=mention, inline=False)

        # if there were any booster
        boosters = data.boosters

        key_user = data.storage.key if data.storage is not None else None



        if boosters is not None:
            if len(boosters) > 0:

                boosters_as_text = []


                for user, code, is_leader in boosters:

                    query = session.query(User).filter(
                        User.username == str(user)
                    ).all()

                    if len(query) == 0:
                        print("not registered")
                        continue

                    boosters_as_text.append(
                        f"{code} {user.mention} | {query[0].realm} {self.key if str(key_user) == str(user) else ''}")

                if len(boosters_as_text) == 0:
                    boosters_as_text = "nope."

                else:
                    boosters_as_text = "\n".join(boosters_as_text)

            else:
                boosters_as_text = "..."

            message.add_field(
                name="Boosters", value=boosters_as_text, inline=False)

        message.add_field(
            name="\u200b", value=f"**Boostid**: `{self.__count}`", inline=True)

        currenct_time = datetime.now()
        message.add_field(
            name="\u200b", value=f"**Today {currenct_time.hour}:{currenct_time.minute}:{currenct_time.second}**", inline=True)
        message.add_field(
            name="\t\t\u200b", value=f"{self.brand} All-inOne community", inline=False)

        return message

    async def send_message(self, ctx, *args):

        print("test")

        self.__count += 1
        count = self.__count

        memory = self.Memory()

        memory.timer_stop = False
        memory.triggered = False

        if len(args) == 6:
            name, armor, price, number_of_boost, realm, char = args
            key = ""

        elif len(args) == 7:
            key, name, armor, price, number_of_boost, realm, char = args

            key_score = int(key.replace("+", ""))
            if key_score > 35:
                await ctx.send("specific key is way more than maximum")

        else:
            await ctx.send("double check your command")

        try:
            message = await self.generate_message(self.Message(ctx), *args)
            storage = BoosterStorage(self.helmet, self.health, self.war)

            post = await self.send_embed_message(ctx, message)

            admin_panel = discord.Embed(
                title=f"Admin panel for boost with boostid `{self.__count}`",
                description=f"only {ctx.author.mention} has access",
                color=Color.purple()
            )

            admin_post = await self.send_embed_message(ctx, admin_panel)

            def check(reaction, user):
                return reaction.message.id == post.id

            def panel_check(reaction, user):
                return reaction.message.id == admin_post.id

            async def update():
                print("calling update message")
                message_data = self.Message(ctx, storage, storage.volunteers)
                new_message = await self.generate_message(message_data, *args)
                await post.edit(embed=new_message)

            async def create_boost():
                # create voice channel
                print("create boost message")

                try:
                    guild = ctx.message.guild
                    channel_name = f"{ctx.author.name}:{count}"

                    role = await guild.create_role(name=channel_name)
                    memory.role = role

                    for user, _, _ in storage.volunteers:
                        await user.add_roles(role)

                    overwrites = {
                        guild.default_role: discord.PermissionOverwrite(read_messages=False),
                        guild.me: discord.PermissionOverwrite(read_messages=True),
                        role: discord.PermissionOverwrite(read_messages=True)

                    }

                    channel = await guild.create_voice_channel(channel_name, overwrites=overwrites)
                    memory.channel = channel

                    invite = await channel.create_invite()

                    await update()

                    users = " ".join(user.mention for user, _,
                                     _ in storage.volunteers)

                    print(users)

                    message = discord.Embed(
                        title="Boost ready",
                        description=f"{users} remember to **set your boost spaces in** and **log the run**. GLHFI!",
                        color=Color.green()

                    )

                    message.add_field(
                        name="Whisper Command", value=f"* leader attention\n`/inv {char}-{realm}`", inline=True)
                    message.add_field(
                        name="Voice channel", value=f"{self.voice} [join voice]({invite})", inline=True)
                    message.add_field(
                        name="\t\t\u200b", value=f"{self.brand} All-inOne community", inline=False)

                    await self.send_embed_message(ctx, message)

                except Exception as error:
                    print(error)

            async def add():
                first_time = True
                key_first_time = True

                while True:

                    if memory.triggered:
                        print("lost loop")
                        break

                    reaction, user = await self.bot.wait_for('reaction_add', check=check)

                    if reaction.emoji in self.boost_items:
                        print("call icon")
                        if not memory.timer_stop:

                            if user == ctx.author:
                                if not memory.timer_stop:
                                    storage.add(
                                        user, reaction.emoji, is_leader=True)

                            else:
                                if not memory.timer_stop:
                                    storage.add(
                                        user, reaction.emoji, is_leader=False)

                        else:
                            print("not accepting icon")

                    else:

                        if reaction.emoji == self.key:
                            print("click on key message")
                            storage.add_key(user)

                        if reaction.emoji == self.cancel:
                            storage.remove_user(user)

                        elif reaction.emoji == self.lock:
                            if user == ctx.author:
                                print("click on lock message")

                                if memory.timer_stop is True:
                                    memory.now = datetime.now()
                                    memory.timer_stop = False

                                else:
                                    print("update message")
                                    await update()
                                    memory.timer_stop = True

                        elif reaction.emoji == self.trigger:

                            print(f"status: {memory.triggered}")

                            if not first_time:
                                if memory.triggered:
                                    print("trigger done.")
                                    break

                                if user == ctx.author:
                                    print("trigger button")

                                    memory.triggered = True
                                    await create_boost()
                                    break
                            else:
                                first_time = False
                                continue

            async def admin_control():

                while True:

                    if memory.triggered:
                        print("lost loop, control panel")
                        break

                    reaction, user = await self.bot.wait_for('reaction_add', check=panel_check)

                    if reaction.emoji == self.health_cross:
                        print("go message")
                        if user == ctx.author:
                            await storage.remove_from_health()
                            await update()
                            continue

                    if reaction.emoji == self.helmet_cross:
                        if user == ctx.author:
                            await storage.remove_from_helmet()
                            await update()
                            continue

                    if reaction.emoji == self.war_cross:
                        if user == ctx.author:
                            await storage.remove_from_war()
                            await update()
                            continue

                    if reaction.emoji == self.war_double_cross:
                        if user == ctx.author:
                            await storage.remove_second_from_war()
                            await update()
                            continue

            async def timer():

                while True:
                    if memory.triggered:
                        break

                    if not memory.triggered:
                        if not memory.timer_stop:
                            if self.Timer.get_difference(memory.now) > 120:
                                print("tik")

                                memory.triggered = True
                                await create_boost()
                                break

                    await asyncio.sleep(2)

            async def stop():
                def check_message(message):
                    content: str = message.content
                    return True if content.startswith("/done") or content.startswith("/fail") else False

                while True:
                    message = await self.bot.wait_for("message", check=check_message)

                    if message.content.startswith('/done'):

                        boost_id = int(message.content.replace("/done ", ""))

                        if boost_id == self.__count:

                            for user, _, _ in storage.volunteers:
                                try:
                                    await user.remove_roles(memory.role)

                                except Exception:
                                    pass

                            await memory.channel.delete()
                            await memory.role.delete()

                            message = discord.Embed(
                                title="Boost finished",
                                description=f"boost with boost id `{self.__count}` finished",
                                color=Color.red()
                            )

                            await self.send_embed_message(ctx, message)

                    if message.content.startswith("/fail"):

                        boost_id = int(message.content.replace("/fail ", ""))

                        if boost_id == self.__count:

                            for user, _, _ in storage.volunteers:
                                try:
                                    await user.remove_roles(memory.role)

                                except Exception:
                                    pass

                            await memory.channel.delete()
                            await memory.role.delete()

                            message = discord.Embed(
                                title="Boost Failed",
                                description=f"boost with boost id `{self.__count}` failed",
                                color=Color.red()
                            )

                            await self.send_embed_message(ctx, message)

            self.bot.loop.create_task(add())
            self.bot.loop.create_task(timer())
            self.bot.loop.create_task(stop())
            self.bot.loop.create_task(admin_control())

            # boost icons
            await post.add_reaction(self.helmet)
            await post.add_reaction(self.health)
            await post.add_reaction(self.war)
            await post.add_reaction(self.key)
            await post.add_reaction(self.cancel)
            await post.add_reaction(self.lock)
            await post.add_reaction(self.trigger)

            # panel icons
            await admin_post.add_reaction(self.helmet_cross)
            await admin_post.add_reaction(self.health_cross)
            await admin_post.add_reaction(self.war_cross)
            await admin_post.add_reaction(self.war_double_cross)

        except ValueError as error:
            print(error)
            embed = discord.Embed(
                title="", description="please fill all fileds")
            await self.send_embed_message(ctx, embed)

        except Exception as error:
            logging.warning("not enough params to unpack")
            print(error)
            return
