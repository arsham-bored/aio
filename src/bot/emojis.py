import discord


class general:
    coin = "\U0001FA99"
    hammer = "⚒️"
    cancel = "🚫"
    lock = "⏱️"
    voice = "🔊"
    key = "🔑"

class CustomeEmoji:
    def __init__(self, name):
        self.name = name

    def to_unicode(self, bot):
        return discord.utils.get(bot.emojis, name=self.name)

class custome:

    helmet = CustomeEmoji('helmet')
    health = CustomeEmoji('health')
    war = CustomeEmoji('war')
    leader = CustomeEmoji('leader')
    coin = CustomeEmoji('boost')
    brand = CustomeEmoji('aio')
    key = CustomeEmoji('game_key')

    helmet_cross = CustomeEmoji("helmet_cross")
    health_cross = CustomeEmoji("health_cross")
    war_cross = CustomeEmoji("war_cross")
    war_double_cross = CustomeEmoji("war_double_cross")