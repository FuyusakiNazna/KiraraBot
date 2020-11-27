# -*- coding: utf-8 -*-
from discord.ext import commands

from kirara.bot import KiraraBot


def get_prefix(bot, message):

    prefixes = bot.prefix

    return commands.when_mentioned_or(*prefixes)(bot, message)


def main():
    bot = KiraraBot(command_prefix=get_prefix)
    bot.run(bot.token)


if __name__ == '__main__':
    main()
