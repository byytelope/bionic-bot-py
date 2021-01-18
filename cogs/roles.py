import os

import discord
import psycopg2
from discord.ext import commands


class Roles(commands.Cog):
    """
    Reaction roles and init role
    """

    def __init__(self, bot: commands.Bot):
        self.bot = bot

        db_database = os.environ["AJU_DB_DATABASE"]
        db_user = os.environ["AJU_DB_USER"]
        db_password = os.environ["AJU_DB_PASSWORD"]
        db_host = os.environ["AJU_DB_HOST"]
        db_port = os.environ["AJU_DB_PORT"]

        try:
            self.db = psycopg2.connect(
                database=db_database,
                user=db_user,
                password=db_password,
                host=db_host,
                port=db_port,
            )
        except psycopg2.OperationalError as db_error:
            print(db_error)

        self.cursor = self.db.cursor()

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        message_id = payload.message_id

        self.cursor.execute(f"SELECT msg_id_reaction FROM main WHERE guild_id = ('{str(payload.guild_id)}')")
        result = self.cursor.fetchone()

        if message_id == int(result[0]):
            guild_id = payload.guild_id
            guild = discord.utils.find(lambda f: f.id == guild_id, self.bot.guilds)

            role = discord.utils.get(guild.roles, name=payload.emoji.name)

            if role is not None:
                member = discord.utils.find(lambda ree: ree.id == payload.user_id, guild.members)
                if member is not None:
                    await member.add_roles(role)
                    print(f"Added {role} to {member}")
                else:
                    print("Member not found.")
            else:
                print("Role not found.")

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
        message_id = payload.message_id

        self.cursor.execute(f"SELECT msg_id_reaction FROM main WHERE guild_id = ('{str(payload.guild_id)}')")
        result = self.cursor.fetchone()

        if message_id == int(result[0]):
            guild_id = payload.guild_id
            guild = discord.utils.find(lambda bruh: bruh.id == guild_id, self.bot.guilds)

            role = discord.utils.get(guild.roles, name=payload.emoji.name)

            if role is not None:
                member = discord.utils.find(lambda ree: ree.id == payload.user_id, guild.members)
                if member is not None:
                    await member.remove_roles(role)
                    print(f"Removed {role} from {member}")
                else:
                    print("Member not found.")
            else:
                print("Role not found.")


def setup(bot):
    bot.add_cog(Roles(bot))
