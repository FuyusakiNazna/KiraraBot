# -*- coding: utf-8 -*-
import io
import math
import re
import sqlite3

import imagehash
import requests
import discord
from discord import Embed
from discord.ext import commands
from PIL import Image

notify_list = ["【超激レア】", "【激レア】", "【レア】"]
last_list = [
    "c0364fac65f4b362",
    "a2f0b526d8976a59",
    "a76e25708a92ff21",
    "c4d90f0c7cb3b4e2",
    "813c64873ee61bec",
    "856e72b033d76cc1",
    "d00f60bf0df01ff0",
    "eb85951a836dda25",
    "85cab6296ac9c9cb",
    "99663ad8668b21f6",
]


def get_hp(hp):
    hp = int(hp)
    unit = ""
    if hp > 1000000:
        hp, unit = hp / 1000000, "M"
    elif hp > 1000:
        hp, unit = hp / 1000, "K"
    hp = "{0:g}".format(math.floor(hp * 10) / (10))
    return hp, unit


def get_rare_em(m, lv, hp, unit, name, rank, imageurl):
    url = f"https://discordapp.com/channels/{m.guild.id}/{m.channel.id}/{m.id}"
    em = Embed(
        description=f"{m.channel.mention}で{rank}{name}が出現しました！\n\n\
            Lv.**{int(lv)}** HP **{hp}{unit}**\n\n\n[**direct link**](<{url}>)",
        timestamp=m.created_at,
    )
    em.set_thumbnail(url=imageurl)
    return em


def get_tohru_em(m, lv, hp, unit, name, imageurl):
    url = f"https://discordapp.com/channels/{m.guild.id}/{m.channel.id}/{m.id}"
    em = Embed(
        description=f"{m.channel.mention}でTohru枠 {name}が出現しました！\n\n\
            Lv.**{int(lv)}** HP **{hp}{unit}**\n\n\n[**direct link**](<{url}>)",
        timestamp=m.created_at,
    )
    em.set_thumbnail(url=imageurl)
    return em


class notifyCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.tao_id = bot.tao_id

    @commands.Cog.listener()
    async def on_message(self, message, level=None, role_name=None):
        if not message.author.id == self.tao_id:
            return
        try:
            if "ランク:【通常】" in message.embeds[0].title:
                return
            if "ランク:【強敵】" in message.embeds[0].title:
                return
            if "ランク:【超強敵】" in message.embeds[0].title:
                return

            imgurl = message.embeds[0].image.url
            img = Image.open(io.BytesIO(requests.get(imgurl).content))
            hash = imagehash.phash(img)
            id = str(hash)

            conn = sqlite3.connect("data/tao.db")
            c = conn.cursor()
            c.execute("SELECT * FROM tao_enemy")
            for row in c.fetchall():
                if id == row[1]:
                    if row[2] in notify_list:
                        lists = re.findall(r"([0-9]+)", f"{message.embeds[0].title}")
                        hp, unit = get_hp(list[1])

                        em = Embed(description=f"**{row[2]}{row[0]}です!**\n\nLv.**{int(lists[0])}** HP **{hp}{unit}**\n**{row[3]}属性")
                        em.set_thumbnail(url=row[5])
                        rare_em = get_rare_em(message, lists[0], hp, unit, row[0], row[2], row[5])
                        cut_strip = row[2].strip("【】")

                        await message.channel.send(embed=em)
                        rolename = f"{cut_strip}報告OK"
                        role = discord.utils.get(message.guild.roles, name=rolename)

                        for channel in message.guild.channels:
                            if channel.name == f"{cut_strip}出現ログ":
                                await channel.send(embed=rare_em)
                                if role in message.guild.roles:
                                    return await channel.send(f"{role.mention}さんたち！{row[2]}{row[0]}です！")

                    elif id in last_list:
                        lists = re.findall(r"([0-9]+)", f"{message.embeds[0].title}")
                        list_num = 1
                        if id == "a76e25708a92ff21":
                            list_num = 2
                        hp, unit = get_hp(list[list_num])

                        em = Embed(description=f"**{row[2]}{row[0]}です!**\n\nLv.**{int(lists[list_num])}** HP **{hp}{unit}**\n**{row[3]}属性")
                        em.set_thumbnail(url=row[5])
                        tohru_em = get_tohru_em(message, lists[list_num], hp, unit, row[0], row[5])

                        await message.channel.send(embed=em)
                        rolename = "tohru枠報告OK"
                        role = discord.utils.get(message.guild.roles, name=rolename)

                        for channel in message.guild.channels:
                            if channel.name == "超激レア出現ログ":
                                await channel.send(embed=tohru_em)
                                if role in message.guild.roles:
                                    return await channel.send(f"{role.mention}さんたち！Tohru枠 {row[0]}です！")
                else:
                    pass

        except Exception:
            pass


def setup(bot):
    bot.add_cog(notifyCog(bot))
