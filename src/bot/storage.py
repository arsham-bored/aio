from datetime import datetime
from . import emojis

class UserBoostStorage:
    users = {}

    @classmethod
    def add(cls, user):
        cls.users.update({ str(user): datetime.now() })

    @classmethod
    def is_allowed(cls, user):
        now = datetime.now()
        last_boost_time: datetime = cls.users.get(user, default=None)

        if last_boost_time is None:
            # user does not exist in memory
            return True

        difference = now - last_boost_time

        if difference.total_seconds() > 30:
            return True

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

    class BoosterNotReady(IndexError):
        pass

    def add(self, user, code, is_leader):
        self.remove_user(user)
        self.data[code].append((user, is_leader))


    def add_key(self, user):

        if user in self.key_:
            self.key_.remove(user)
            return

        else:
            self.key_.append(user)
            return

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


    def helmet_volunteer(self):
        if len(self.data[self.helmet]) > 0:
            while True:
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

            while True:
                boosters = self.data[self.war][:2]

                for user in boosters:
                    if not UserBoostStorage.is_allowed(user):
                        self.remove_user(user)

                    else:
                        valids.append(user)
                    

                if len(valids) == 2:
                    return [(user, self.war, False) for user in valids]
        
        return []

    @property
    def volunteers(self):
        try:
            helmet = self.helmet_volunteer()
            health = self.health_volunteer()
            war = self.war_volunteer()

            return [*helmet, *health, *war]

        except IndexError as error:
            print(error)
            print(self.data)
            raise self.BoosterNotReady("not enough volunteer")

        except Exception as error:
            print(error)
    