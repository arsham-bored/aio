from . import emojis

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
            user, is_leader = self.data[self.helmet][0]
            return [(user, self.helmet, is_leader)]

        return []

    def health_volunteer(self):
        if len(self.data[self.health]) > 0:
            user, is_leader = self.data[self.health][0]
            return [(user, self.health, is_leader)]

        return []

    def war_volunteer(self):
        if len(self.data[self.war]) > 0:
            boosters = self.data[self.war][:2]
            return [(user, self.war, is_leader) for user, is_leader in boosters]

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
        