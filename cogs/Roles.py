import discord
from discord.ext import commands

default_role = 'Fukushima Daichi'

class Roles(commands.Cog):
    """
    Reaction roles and init role
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        role = discord.utils.get(member.guild.roles, name=default_role)
        await member.add_roles(role)
        print(f'{member} was given {role}')

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        message_id = payload.message_id
        if message_id == 711977846112911490:
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
        if message_id == 711977846112911490:
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