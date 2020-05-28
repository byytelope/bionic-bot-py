import discord
import psycopg2
import os
from discord.ext import commands

class Roles(commands.Cog):
    """
    Reaction roles and init role
    """
    def __init__(self, bot):
        self.bot = bot

        db_database = os.environ['db_database']
        db_user = os.environ['db_user']
        db_password = os.environ['db_password']
        db_host = os.environ['db_host']
        db_port = os.environ['db_port']

        try:
            self.db = psycopg2.connect(
                database=db_database,
                user=db_user,
                password=db_password, 
                host=db_host,
                port=db_port
                )
            print('db con succ')
        except psycopg2.OperationalError as e:
            print(e)
            print('db con not succ')

        self.cursor = self.db.cursor()

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
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
    async def on_raw_reaction_remove(self, payload):
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