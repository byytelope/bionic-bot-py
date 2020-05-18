import discord
from discord.ext import commands

bot = commands.Bot(command_prefix=".")

class ReactionRoles(commands.Cog):
    """
    Reaction roles and message id setter
    """
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(aliases='roleid')
    async def set_message_id(self, ctx, id_: int):
        global message_id_setter
        message_id_setter = id_

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        message_id = payload.message_id
        if message_id == message_id_setter:
            guild_id = payload.guild_id
            guild = discord.utils.find(lambda bruh: bruh.id == guild_id, bot.guilds)

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
        if message_id == message_id_setter:
            guild_id = payload.guild_id
            guild = discord.utils.find(lambda bruh: bruh.id == guild_id, bot.guilds)

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
    bot.add_cog(ReactionRoles(bot))