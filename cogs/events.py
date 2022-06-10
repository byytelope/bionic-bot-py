import sys
import os

import discord
from discord.ext import commands


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from bot import BionicBot


class Events(commands.Cog):
    def __init__(self, bot: BionicBot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member) -> None:
        print(f"{member} has joined {member.guild}")


async def setup(bot: BionicBot) -> None:
    await bot.add_cog(Events(bot))
