import discord
import psycopg2
import os
from discord.ext import commands

class Set(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        DATABASE_URL = os.getenv("DATABASE_URL")
        self.db = psycopg2.connect(DATABASE_URL, sslmode="require")
        self.cursor = self.db.cursor()

    @commands.group(invoke_without_command=True)
    async def set(self, ctx):
        embed = discord.Embed(
            title = 'set **<command>**',
            colour = discord.Colour.blurple()
            )
        embed.set_footer(text=f'{ctx.guild}', icon_url=f'{ctx.guild.icon_url}')
        embed.add_field(name='welctext', value='Set welcome text.', inline=False)
        embed.add_field(name='welcch', value='Set welcome channel.', inline=False)

        await ctx.send(embed=embed)

    @set.command(aliases=['welctext'])
    @commands.has_any_role('Chernobyl', 'Three Mile Island')
    async def set_welc_text(self, ctx, *, welc_text):

        self.cursor.execute(f"SELECT welc_text FROM main WHERE guild_id = {ctx.guild.id}")
        result = self.cursor.fetchone()

        audit_ch = self.bot.get_channel(712599778868854794)

        if result is None:
            sql = ("INSERT INTO main(guild_id, welc_text) VALUES(?,?)")
            val = (ctx.guild.id, welc_text)
            await ctx.send(f"""
                Welcome text has been set to **"{welc_text}"**
                """)

            embed = discord.Embed(
            title=ctx.author,
            description=f'set welcome channel to **"{welc_text}"**',
            colour=discord.Colour.blurple()
            )
            await audit_ch.send(embed=embed)

        elif result is not None:
            sql = ("UPDATE main SET welc_text = ? WHERE guild_id = ?")
            val = ( welc_text, ctx.guild.id)
            await ctx.send(f"""
                Welcome text has been changed to "{welc_text}"
                """)

            embed = discord.Embed(
            title=ctx.author,
            description=f'changed welcome text to **"{welc_text}"**',
            colour=discord.Colour.blurple()
            )
            await audit_ch.send(embed=embed)
    
        self.cursor.execute(sql, val)
        self.db.commit()
        self.cursor.close()
        self.db.close()

    @set.command(aliases=['welcch'])
    @commands.has_any_role('Chernobyl', 'Three Mile Island')
    async def set_welc_ch(self, ctx, welc_ch: discord.TextChannel):
        self.cursor.execute(f"SELECT ch_id_welc FROM main WHERE guild_id = {ctx.guild.id}")
        result = self.cursor.fetchone()

        audit_ch = self.bot.get_channel(712599778868854794)

        if result is None:
            sql = ("INSERT INTO main(guild_id, ch_id_welc) VALUES(?,?)")
            val = (ctx.guild.id, welc_ch)
            await ctx.send(f"Welcome channel has been set to {welc_ch.mention}")

            embed = discord.Embed(
            title=ctx.author,
            description=f'set welcome channel to {welc_ch.mention}',
            colour=discord.Colour.blurple()
            )
            await audit_ch.send(embed=embed)

        elif result is not None:
            sql = ("UPDATE main SET ch_id_welc = ? WHERE guild_id = ?")
            val = (welc_ch, ctx.guild.id)
            await ctx.send(f"Welcome channel has been changed to {welc_ch.mention}")

            embed = discord.Embed(
            title=ctx.author,
            description=f'changed welcome channel to {welc_ch.mention}',
            colour=discord.Colour.blurple()
            )
            await audit_ch.send(embed=embed)

        self.cursor.execute(sql, val)
        self.db.commit()
        self.cursor.close()
        self.db.close()


def setup(bot):
    bot.add_cog(Set(bot))