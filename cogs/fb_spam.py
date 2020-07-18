import os

import discord
from discord.ext import commands
from fbchat import Client, Message
from fbchat.models import *


class FBSpam(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.client = Client(os.environ["ree_email"], os.environ["ree_pass"])
        self.thread_id = "3047607055302251"
        self.thread_type = ThreadType.GROUP

    @commands.command(name="fbspam", aliases=["fbs", "messenger"])
    @commands.has_guild_permissions(manage_guild=True)
    async def fb_spam(self, ctx, _num, *, _user):
        num = int(_num)
        group_info = self.client.fetchThreadInfo(self.thread_id)[self.thread_id]
        users = group_info.nicknames
        user_id = [k for (k, v) in users.items() if _user.lower() in v.lower()][0]

        length = len(_user) + 1
        for i in range(0, num):
            self.client.send(
                Message(text=f"@{_user}", mentions=[Mention(thread_id=user_id, offset=0, length=length)]),
                thread_id=self.thread_id,
                thread_type=self.thread_type,
            )
        await ctx.send(f"Spammed {_user} {num} times.")


def setup(bot):
    bot.add_cog(FBSpam(bot))
