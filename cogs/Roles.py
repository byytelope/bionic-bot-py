import discord
from discord.ext import commands

bot = commands.Bot(command_prefix=".")
default_role = 'Kyshtym'

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


def setup(bot):
    bot.add_cog(Roles(bot)) 