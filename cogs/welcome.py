import os
import discord
import psycopg2
from discord.ext import commands


class Welcome(commands.Cog):
    """
    Welcome actions
    """

    def __init__(self, bot):
        self.bot = bot

        db_database = os.environ["db_database"]
        db_user = os.environ["db_user"]
        db_password = os.environ["db_password"]
        db_host = os.environ["db_host"]
        db_port = os.environ["db_port"]

        try:
            self.db = psycopg2.connect(
                database=db_database, user=db_user, password=db_password, host=db_host, port=db_port,
            )
        except psycopg2.OperationalError as db_error:
            print(db_error)

        self.cursor = self.db.cursor()

    @commands.Cog.listener()
    async def on_member_join(self, member):
        self.cursor.execute(f"SELECT role_id_default FROM main WHERE guild_id = ('{str(member.guild.id)}')")
        result_2 = self.cursor.fetchone()
        if result_2 is None:
            return
        else:
            default_role = discord.utils.get(member.guild.roles, id=int(result_2[0]))
            # role = discord.utils.get(member.guild.roles, name=default_role)
            await member.add_roles(default_role)
            print(f"{member} was given {default_role}")

        self.cursor.execute(f"SELECT ch_id_welcome FROM main WHERE guild_id = ('{str(member.guild.id)}')")
        result = self.cursor.fetchone()
        if result is None:
            return
        else:
            self.cursor.execute(f"SELECT welc_text FROM main WHERE guild_id = ('{str(member.guild.id)}')")
            result_1 = self.cursor.fetchone()
            welc_ch = self.bot.get_channel(id=int(result[0]))
            msg = str(result_1[0]).format(mention=member.mention, user=member.name, guild=member.guild)

            embed = discord.Embed(
                title=f"Welcome to {member.guild}!", description=msg, colour=discord.Colour(0xE9ACFD),
            )
            embed.set_thumbnail(url=member.avatar_url)
            embed.set_footer(text=member.guild, icon_url=member.guild.icon_url)
            await welc_ch.send(embed=embed)


def setup(bot):
    bot.add_cog(Welcome(bot))
