import discord
import sqlite3
import datetime
from discord.ext import commands

default_role = 'Fukushima Daichi'

class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['welctext'])
    @commands.has_any_role('Chernobyl', 'Three Mile Island')
    async def set_welc_text(self, ctx, *, welc_text):
        db = sqlite3.connect('db.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT welc_text FROM main WHERE guild_id = {ctx.guild.id}")
        result = cursor.fetchone()
        if result is None:
            sql = ("INSERT INTO main(guild_id, welc_text) VALUES(?,?)")
            val = (ctx.guild.id, welc_text)
            await ctx.send(f"""
                Welcome text has been set to "{welc_text}"
                """)
        elif result is not None:
            sql = ("UPDATE main SET welc_text = ? WHERE guild_id = ?")
            val = ( welc_text, ctx.guild.id)
            await ctx.send(f"""
                Welcome text has been changed to "{welc_text}"
                """)
        cursor.execute(sql, val)
        db.commit()
        cursor.close()
        db.close()

    @commands.command(aliases=['welcch'])
    @commands.has_any_role('Chernobyl', 'Three Mile Island')
    async def set_welc_ch(self, ctx, welc_ch: discord.TextChannel):
        db = sqlite3.connect('db.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT ch_id_welc FROM main WHERE guild_id = {ctx.guild.id}")
        result = cursor.fetchone()
        if result is None:
            sql = ("INSERT INTO main(guild_id, ch_id_welc) VALUES(?,?)")
            val = (ctx.guild.id, welc_ch)
            await ctx.send(f"Welcome channel has been set to {welc_ch.mention}")
        elif result is not None:
            sql = ("UPDATE main SET ch_id_welc = ? WHERE guild_id = ?")
            val = (welc_ch, ctx.guild.id)
            await ctx.send(f"Welcome channel has been changed to {welc_ch.mention}")
        cursor.execute(sql, val)
        db.commit()
        cursor.close()
        db.close()

    @commands.Cog.listener()
    async def on_member_join(self, member):
        role = discord.utils.get(member.guild.roles, name=default_role)
        embed = discord.Embed(description = f'Welcome to Bionic {member.mention}!', colour = discord.Colour.blurple)
        embed.set_thumbnail(url=f'{member.avatar_url}')
        embed.set_author(name=f'{member.name}', icon_url=f'{member.avatar_url}')
        embed.set_footer(text=f'{member.guild}', icon_url=f'{member.guild.icon_url}')
        # embed.timestamp = datetime.datetime.now()

        await member.add_roles(role)
        print(f'{member} was given {role}')

        # db = sqlite3.connect('db.sqlite')
        # cursor = db.cursor()
        # cursor.execute(f"SELECT ch_id_welc FROM main WHERE guild_id = {member.guild.id}")
        # result = cursor.fetchone()

        welc_ch = self.bot.get_channel(592074944217612298)
        await welc_ch.send(embed=embed)


def setup(bot):
    bot.add_cog(Welcome(bot))