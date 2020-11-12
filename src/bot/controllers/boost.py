from typing import List
import discord
from discord import Color
from discord.ext import tasks
from datetime import datetime
import asyncio
from ... import config
from ...orm.engine import session
from ...orm.models.user import User, get_user
from ...orm.models.boost import Boost
from ...orm.models.transaction import Transaction
from .. import emojis
from ..storage import (
    BoosterStorage,
    UserBoostStorage
)
from ..utils import to_k
from .base import Controller
import logging
import uuid


class Booster(Controller):

    def __init__(self, bot):
        self.bot = bot

        # controll icons
        self.trigger = emojis.general.hammer
        self.cancel = emojis.general.cancel
        self.lock = emojis.general.lock
        self.voice = emojis.general.voice

        query: List[Boost] = session.query(Boost).order_by(Boost.id.desc()).limit(1).all()

        self.count = query[0].id

    class Message:
        def __init__(self, ctx, storage=None, boosters=None):
            self.ctx = ctx
            self.boosters = boosters
            self.storage: BoosterStorage = storage
            self.done = False
            self.memory = []
            self.vol = []

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
            self.done = False
            self.last_stage = False
            self.count = None
            self.key_user = None
            self.reactions = []

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

    async def send_message(self, ctx, *args):

        print("test")

        self.count += 1

        memory = self.Memory()
        memory.count = self.count

        user_memory = []

        pre_memory = []

        memory.timer_stop = False
        memory.triggered = False

        print(str(ctx.author))

        advertiser_registery = session.query(User).filter(
            User.username == str(ctx.author)
        ).all()

        print(advertiser_registery)

        if len(advertiser_registery) == 0:
            await ctx.send(f"{ctx.author.name}, please register before any boost commit.")
            return 

        advertiser_user: User = advertiser_registery[0]

        async def generate_message(data: self.Message, *args) -> discord.Embed:

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

            self.helmet_cross = emojis.custome.helmet_cross.to_unicode(
                self.bot)
            self.health_cross = emojis.custome.health_cross.to_unicode(
                self.bot)
            self.war_cross = emojis.custome.war_cross.to_unicode(self.bot)
            self.war_double_cross = emojis.custome.war_double_cross.to_unicode(
                self.bot)

            self.boost_items = self.BoostItems(
                self.helmet, self.health, self.war)

            message = discord.Embed(title=f"{ctx.author.name}'s Boost",
                                    description=f"**{key}{' - ' if key != '' else ''} {name.capitalize()}**", color=Color.orange())
            message.add_field(
                name=f"\u200b", value=f"**Booster Cut:** {to_k(self.calculate_cut(int(price)))} {self.coin}", inline=False)
            message.add_field(name="Armor Stack\t\t\t\t\t  ",
                              value=self.status(armor), inline=True)
            message.add_field(name="Boost Price\t\t\t\t\t  ",
                              value=f"{to_k(price)} {self.coin}", inline=True)
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
            boosters = data.boosters if not memory.last_stage else storage.pre

            print(memory.last_stage)

            print(boosters)

            def get():
                if boosters is not None:
                    for user, _, _ in boosters:
                        if user == storage.key:
                            print("got user")
                            return user

                return None

            key_user = get()
            memory.key_user = key_user

            print("key user:")
            print(str(key_user))

            print(boosters, storage.pre if not data.storage is False else "")

            if boosters is not None:
                if len(boosters) > 0:

                    boosters_as_text = []

                    leader_user = None

                    for user, _, _ in boosters:

                        if isinstance(user, tuple):
                            user, _ = user

                        query = session.query(User).filter(
                            User.username == str(user)
                        ).all()

                        if len(query) == 0:
                            print("not registered, score action for user", str(user))
                            continue

                        current_user = query[0]
                        print(current_user.score)

                        if leader_user is None:
                            leader_user = current_user
                            continue

                        if current_user.score > leader_user.score:
                            leader_user = current_user

                    print("users:\n")
                    print(boosters)

                    for user, code, is_leader in boosters:

                        if isinstance(user, tuple):
                            user, _ = user

                        query = session.query(User).filter(
                            User.username == str(user)
                        ).all()

                        if data.done:
                            print("limiting all users.")
                            UserBoostStorage.add(user)

                        if not memory.last_stage:
                            storage.pre.append((user, code, is_leader))

                        if len(query) == 0:
                            print("not registered for user", user)
                            continue

                        user_memory.append(user)

                        is_leader = query[0] == leader_user

                        print("leader check")
                        print("status: ", is_leader)

                        if str(key_user) == str(user):
                            print("giving key to ..", str(user))

                        boosters_as_text.append(
                            f"{code} {user.mention} | {query[0].realm} {self.leader if is_leader else ''} {self.key if str(key_user) == str(user) else ''}")

                    if len(boosters_as_text) == 0:
                        boosters_as_text = "nope."

                    else:
                        boosters_as_text = "\n".join(boosters_as_text)

                else:
                    boosters_as_text = "..."

                message.add_field(
                    name="Boosters", value=boosters_as_text, inline=False)

            message.add_field(
                name="\u200b", value=f"**Boostid**: `{memory.count}`", inline=True)

            currenct_time = datetime.now().strftime("%H:%M:%S")
            message.add_field(
                name="\u200b", value=f"**Today {currenct_time}**", inline=True)
            message.add_field(
                name="\t\t\u200b", value=f"{self.brand} All-inOne community", inline=False)

            return message

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
            message = await generate_message(self.Message(ctx, False), *args)
            storage = BoosterStorage(self.helmet, self.health, self.war)

            post = await self.send_embed_message(ctx, message)

            admin_panel = discord.Embed(
                title=f"Admin panel for boost with boostid `{memory.count}`",
                description=f"only {ctx.author.mention} has access",
                color=Color.purple()
            )

            admin_post = await self.send_embed_message(ctx, admin_panel)

            def check(reaction, user):
                return reaction.message.id == post.id

            def panel_check(reaction, user):
                return reaction.message.id == admin_post.id

            async def update(done=False):
                print("calling update message")
                message_data = self.Message(
                    ctx, storage, storage.volunteers)

                new_message = await generate_message(message_data, *args)

                user_memory = message_data.memory

                await post.edit(embed=new_message)

            async def create_boost():
                # create voice channel
                print("create boost message")

                try:
                    guild = ctx.message.guild
                    channel_name = f"{ctx.author.name}:{memory.count}"

                    role = await guild.create_role(name=channel_name)
                    memory.role = role

                    users = [user for user, _, _ in storage.pre]

                    if len(users) == 0:
                        message = discord.Embed(
                            title="Boost failed",
                            description=f"no volunteer",
                            color=Color.red()

                        )

                        await admin_post.edit(embed=message)
                        await admin_post.remove_reaction(self.health_cross, self.bot.user)
                        await admin_post.remove_reaction(self.helmet_cross, self.bot.user)
                        await admin_post.remove_reaction(self.war_cross, self.bot.user)
                        await admin_post.remove_reaction(self.war_double_cross, self.bot.user)             

                    print(f"user to give role: \n{users}")

                    for user in users:
                        print(f"giving role to .. {user}")
                        await user.add_roles(role)

                    overwrites = {
                        guild.default_role: discord.PermissionOverwrite(read_messages=False),
                        guild.me: discord.PermissionOverwrite(read_messages=False),
                        role: discord.PermissionOverwrite(read_messages=True)

                    }

                    channel = await guild.create_voice_channel(channel_name, overwrites=overwrites)
                    memory.channel = channel

                    invite = await channel.create_invite()

                    await update()

                    users = " ".join(user.mention for user in users)

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

                    await admin_post.edit(embed=message)
                    await admin_post.remove_reaction(self.health_cross, self.bot.user)
                    await admin_post.remove_reaction(self.helmet_cross, self.bot.user)
                    await admin_post.remove_reaction(self.war_cross, self.bot.user)
                    await admin_post.remove_reaction(self.war_double_cross, self.bot.user)

                except Exception as error:
                    print(error)

            async def add():
                first_time = True
                key_first_time = True

                while True:

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
                            storage.remove_key_user(user)

                        elif reaction.emoji == self.lock:
                            if user == ctx.author:
                                print("click on lock message")

                                if memory.timer_stop is True:
                                    memory.now = datetime.now()
                                    memory.timer_stop = False

                                else:
                                    message_data = self.Message(
                                        ctx, storage, storage.volunteers)

                                    message_data.done = True

                                    new_message = await generate_message(message_data, *args)

                                    user_memory = message_data.memory

                                    await post.edit(embed=new_message)

                                    memory.timer_stop = True

                                memory.last_stage = True

                        elif reaction.emoji == self.trigger:

                            print(f"status: {memory.triggered}")

                            if True:

                                if user == ctx.author:
                                    print("trigger button")

                                    message_data = self.Message(
                                        ctx, storage, storage.volunteers)

                                    message_data.done = True

                                    new_message = await generate_message(message_data, *args)

                                    user_memory = message_data.memory

                                    print("trigger .. .. ..")

                                    await post.edit(embed=new_message)

                                    memory.timer_stop = True
                                    memory.triggered = True

                                    memory.last_stage = True
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
                        if str(user) != "Jaina Proudmore boost#0365":
                            print("go message")
                            if user == ctx.author:

                                healers = storage.pre_get_user(self.health)

                                if len(healers) != 0:
                                    UserBoostStorage.remove(healers[0])
                                    await storage.pre_remove_from_health()
                                    storage.remove_key_user(healers[0])

                                    await update()
                                    continue

                    if reaction.emoji == self.helmet_cross:
                        if str(user) != "Jaina Proudmore boost#0365":
                            if user == ctx.author:

                                tanks = storage.pre_get_user(self.helmet)

                                if len(tanks) != 0:
                                    UserBoostStorage.remove(tanks[0])
                                    await storage.pre_remove_from_helmet()
                                    storage.remove_key_user(tanks[0])

                                    await update()
                                    continue

                    if reaction.emoji == self.war_cross:
                        if str(user) != "Jaina Proudmore boost#0365":
                            if user == ctx.author:
                                dpss = storage.pre_get_user(self.war)

                                if len(dpss) != 0:
                                    UserBoostStorage.remove(dpss[0])
                                    await storage.pre_remove_from_war()
                                    storage.remove_key_user(dpss[0])

                                    await update()
                                    continue

                    if reaction.emoji == self.war_double_cross:
                        if str(user) != "Jaina Proudmore boost#0365":
                            if user == ctx.author:
                                dpss = storage.pre_get_user(self.war)

                                if len(dpss) > 1:
                                    UserBoostStorage.remove(dpss[1])
                                    await storage.pre_remove_second_from_war()
                                    storage.remove_key_user(dpss[1])

                                    await update()
                                    continue

            async def timer():

                while True:
                    if memory.triggered:
                        break

                    if not memory.triggered:
                        if not memory.timer_stop:
                            if self.Timer.get_difference(memory.now) > config.boost_time:
                                print("tik")
                                message_data = self.Message(
                                    ctx, storage, storage.volunteers
                                )

                                message_data.done = True

                                new_message = await generate_message(message_data, *args)

                                user_memory = message_data.memory

                                await post.edit(embed=new_message)

                                memory.timer_stop = True

                                memory.last_stage = True
                                memory.triggered = True
                                await create_boost()
                                break

                    await asyncio.sleep(2)

            async def commit_transaction():

                print("record transactions..")

                for user, _, _ in storage.pre:
                    transaction = Transaction()
                    user_registery = get_user(str(user))[0]

                    transaction.user_id = user_registery.id 
                    transaction.price = self.calculate_cut(int(price))

                    print("add to session ..")
                    session.add(transaction)

                print("commit transactions")
                session.commit()
                
            async def commit_boost(failed=False):

                print("record boost..")

                boost = Boost()
                boost.is_failed =  failed
                boost.price = price
                boost.cut = self.calculate_cut(int(price))
                boost.armor = armor
                boost.realm = realm
                boost.char = char
                boost.required_key = int(key.replace("+", ""))
                boost.advertiser_id = advertiser_user.id
                
                second = False

                for user, code, _ in storage.pre:
                    user_registery = get_user(str(user))[0]

                    if code == self.health:
                        boost.healer_id = user_registery.id

                    if code == self.helmet:
                        boost.tank_id = user_registery.id

                    if code == self.war:
                        if not second:
                            boost.dps_1_id = user_registery.id
                            second = True
                            continue

                        boost.dps_2_id = user_registery.id

                    if str(user) == str(memory.key_user):
                        print("giving key in record..")
                        boost.key_id = user_registery.id

                session.add(boost)
                session.commit()


            async def stop():
                def check_message(message):
                    content: str = message.content
                    return True if content.startswith("/done") or content.startswith("/fail") else False

                while True:
                    message = await self.bot.wait_for("message", check=check_message)

                    if not message.author.server_permissions.administrator:
                        continue

                    content = message.content

                    try:
                        
                        if memory.triggered:
                            if content.startswith('/done'):

                                boost_id = int(content.replace("/done ", ""))
                                print(
                                    f"boost with boost id {memory.count} done -> got value {boost_id}")

                                if boost_id == memory.count:

                                    await memory.channel.delete()
                                    await memory.role.delete()

                                    await commit_boost()
                                    await commit_transaction()

                                    message = discord.Embed(
                                        title="Boost finished",
                                        description=f"boost finished",
                                        color=Color.red()
                                    )

                                    await admin_post.edit(embed=message)
                                    break

                            if content.startswith("/fail"):

                                boost_id = int(content.replace("/fail ", ""))

                                if boost_id == memory.count:


                                    await memory.channel.delete()
                                    await memory.role.delete()

                                    await commit_boost(failed=True)

                                    message = discord.Embed(
                                        title="Boost Failed",
                                        description=f"boost with boost id `{memory.count}` failed",
                                        color=Color.red()
                                    )

                                    await admin_post.edit(embed=message)
                                    break

                    except Exception as error:
                        print(error)
                        pass

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

            await admin_post.add_reaction(self.helmet_cross),
            await admin_post.add_reaction(self.health_cross),
            await admin_post.add_reaction(self.war_cross),
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
