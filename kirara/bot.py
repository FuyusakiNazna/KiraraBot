# -*- coding: utf-8 -*-
import discord
import toml
from discord.ext import commands, tasks

with open("config.toml") as config_file:
    config = toml.loads(config_file.read())['bot']


class KiraraBot(commands.Bot):
    def __init__(self, command_prefix):
        super().__init__(command_prefix)
        self.remove_command('help')
        self.token = config['token']
        self.prefix = config['prefix']
        self.cog = config['cogs']
        self.tao_id = config['tao_id']
        self.loadcog = []
        self.ready = False

    async def on_ready(self):
        for c in self.cog:
            try:
                self.load_extension(c)
                self.loadcog.append(c)
            except commands.ExtensionAlreadyLoaded:
                pass

        self.playing.start()
        self.ready = True
        print(f"{self.user.name}#{self.user.discriminator} has started...")
        print("Kirara project: https://github.com/FuyusakiNazna/KiraraBot")
        print("loaded cogs: {}".format(", ".join(self.loadcog)))

    async def on_command_error(self, ctx, error):
        if not self.ready:
            return

        if isinstance(error, commands.CommandNotFound):
            return

        if isinstance(error, commands.NoPrivateMessage):
            try:
                await ctx.author.send("This command cannot be used in DM.")
            except discord.Forbidden:
                pass
            return

    @tasks.loop(seconds=60.0)
    async def playing(self):
        await self.wait_until_ready()
        await self.change_presence(activity=discord.Game(name="kirara.py"))
