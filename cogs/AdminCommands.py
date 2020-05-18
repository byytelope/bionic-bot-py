import discord
from discord.ext import commands

class AdminCommands(commands.Cog):
    """
    Admin commands for admins
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['clear'])
    @commands.has_any_role('Chernobyl', 'Three Mile Island', 'Covid-19')
    @commands.has_permissions(manage_messages=True)
    async def cls(self, ctx, amount=3):
        await ctx.channel.purge(limit=amount)

    @cls.error
    async def on_cls_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions) or isinstance(error, commands.MissingAnyRole):
            await ctx.send("Adhi the command beynun vey varah ekalo bondo nivei.")


def setup(bot):
    bot.add_cog(AdminCommands(bot))