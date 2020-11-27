# -*- coding: utf-8 -*-
from discord.ext import commands


class ownerCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["s"])
    @commands.is_owner()
    async def say(self, ctx, *, text):
        return await ctx.send(text)


def setup(bot):
    bot.add_cog(ownerCog(bot))
