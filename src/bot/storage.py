from datetime import datetime
from . import emojis
from .. import config

class UserBoostStorage:
    users = {}

    @classmethod
    def add(cls, user):
        cls.users.update({ str(user): datetime.now() })

    @classmethod
    def remove(cls, user):
        if str(user) in cls.users:
            print("remove user")
            del cls.users[str(user)]

    @classmethod
    def is_allowed(cls, user):
        user = str(user)
        now = datetime.now()
        last_boost_time: datetime = cls.users.get(user, None)

        if last_boost_time is None:
            print(f"{user} allowed, beacause not exists in memory")
            # user does not exist in memory
            return True

        difference = now - last_boost_time

        if difference.total_seconds() > config.limit_time:
            print(f"{user} allowed")
            return True


        print(f"{user} not allowed")
        return False
    

class BoosterStorage:
    def __init__(self, helmet, health, war):
        self.helmet = helmet
        self.health = health
        self.war = war

        self.data = {
            helmet: [],
            health: [],
            war: []
        }

        self.key_ = []

        self.pre = []

    class BoosterNotReady(IndexError):
        pass

    def add(self, user, code, is_leader):

        if str(user) == config.name:
            return

        self.remove_user(user)
        self.data[code].append((user, is_leader))
        print("adding user", str(user))


    def add_key(self, user):

        if str(user) == config.name:
            return

        if user in self.key_:
            self.key_.remove(user)
            return

        else:
            self.key_.append(user)
            return

    def remove_key_user(self, user):
        if user in self.key_:
            print("delething key user: ", str(user))
            self.key_.remove(user)

            print("next volunteers: \n")
            print("".join(f"{user}\n" for user in self.key_))

    @property
    def key(self):
        try:
            return self.key_[0]
        except:
            return None

    def remove(self, code):
        for icon in self.data:
            if icon == code:
                self.data[icon].pop(0)

    def remove_user(self, user):
        for icon in self.data:
            users = self.data[icon]
            for pre_user, pre_is_leader in users:
                if pre_user == user:
                    users.remove((pre_user, pre_is_leader))
                

    def remove_pre(self, user):
            for pre_user, icon, _ in self.pre:
                if pre_user == user:
                    print(f"deleting user {user}")
                    self.pre.remove((pre_user, icon, _))

    async def remove_from_health(self):
        try:
            del self.data[self.health][0]
        except:
            return

    async def remove_from_helmet(self):
        try:
            del self.data[self.helmet][0]
        except: 
            return

    async def remove_from_war(self):
        try:
            del self.data[self.war][0]
        except:
            return

    async def remove_second_from_war(self):
        try:
            del self.data[self.war][1]
        except:
            return


    def pre_get_user(self, code):
        return [user for user, code_, is_leader in self.pre if code == code_]

    async def pre_remove_from_health(self):
        for index, (user, code, _) in enumerate(self.pre):
            if code == self.health:
                print("delet user ..")
                print("before: ", self.pre)
                del self.pre[index]

                print("after: ", self.pre)

    async def pre_remove_from_helmet(self):
        for index, (user, code, _) in enumerate(self.pre):
            if code == self.helmet:
                del self.pre[index]

    async def pre_remove_from_war(self):
        for index, (user, code, _) in enumerate(self.pre):
            if code == self.war:
                del self.pre[index]

    async def pre_remove_second_from_war(self):
        second = False

        for index, (user, code, _) in enumerate(self.pre):
            if code == self.war:
                if second:
                    print("delete second dps user")
                    del self.pre[index]
                else:
                    print("going for second user")
                    second = True

    def helmet_volunteer(self):
        if len(self.data[self.helmet]) > 0:
            while True:
                if len(self.data[self.helmet]) == 0:
                    return []

                user, is_leader = self.data[self.helmet][0]


                if not UserBoostStorage.is_allowed(user):
                    self.remove_user(user)
                    continue

                if UserBoostStorage.is_allowed(user):
                    return [(user, self.helmet, is_leader)]

        return []

    def health_volunteer(self):
        if len(self.data[self.health]) > 0:
            while True:
                if len(self.data[self.health]) == 0:
                    return []

                user, is_leader = self.data[self.health][0]


                if not UserBoostStorage.is_allowed(user):
                    self.remove_user(user)
                    continue

                if UserBoostStorage.is_allowed(user):
                    return [(user, self.health, is_leader)]

        return []

    def war_volunteer(self):
        if len(self.data[self.war]) > 0:

            valids = []

            for user, is_leader in self.data[self.war]:
                if UserBoostStorage.is_allowed(user):
                    print(f"adding user: {user}")
                    valids.append(user)

            return [(user, self.war, False) for user in valids[:2]]
        
        return []

    @property
    def volunteers(self):
        try:
            helmet = self.helmet_volunteer()
            health = self.health_volunteer()
            war = self.war_volunteer()

            print(
                helmet,
                health,
                war
            )

            return [*helmet, *health, *war]

        except IndexError as error:
            print(error)
            print(self.data)
            raise self.BoosterNotReady("not enough volunteer")

        except Exception as error:
            print(error)
    