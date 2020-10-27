import discord


class general:
    coin = "\U0001FA99"

class custome:

    shield: str = 'helmet'
    health: str = 'health'
    war: str = 'war'
    leader: str = 'leader'
    coin = 'boost'

    @staticmethod
    def get(bot, emoji_name):
        return discord.utils.get(bot.emojis, name=emoji_name)