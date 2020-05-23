import discord
import psycopg2
import datetime
import os
from discord.ext import commands

default_role = 'Fukushima Daichi'

class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        DATABASE_URL = os.getenv("DATABASE_URL")
        self.db = psycopg2.connect(DATABASE_URL, sslmode="require")
        self.cursor = self.db.cursor()
        
    @commands.Cog.listener()
    async def on_member_join(self, member):
        role = discord.utils.get(member.guild.roles, name=default_role)
        await member.add_roles(role)
        print(f'{member} was given {role}')

        self.cursor.execute(f'SELECT ch_id_welcome FROM main WHERE guild_id = {member.guild.id}')
        result = self.cursor.fetchone()
        if result is None:
            return
        else:
            self.cursor.execute(f'SELECT welc_text FROM main WHERE guild_id = {member.guild.id}')
            result_1 = self.cursor.fetchone()

            embed = discord.Embed(description = f'{str(result_1[0])}', colour = discord.Colour.blurple())
            embed.set_thumbnail(url=f'{member.avatar_url}')
            embed.set_footer(text=f'{member.guild}', icon_url=f'{member.guild.icon_url}')
            # embed.timestamp = datetime.datetime.now()

            # welc_ch = self.bot.get_channel(592074944217612298)
            welc_ch = self.bot.get_channel(id=int(result[0]))
            await welc_ch.send(embed=embed)


def setup(bot):
    bot.add_cog(Welcome(bot))