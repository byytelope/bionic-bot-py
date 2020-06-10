import discord
from discord.ext import commands

class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['ttt'])
    async def tictactoe(self, ctx):
        board = '''
`3` `   ` `   ` `   `
`2` `   ` `   ` `   `
`1` `   ` `   ` `   `
` ` ` A ` ` B ` ` C `
'''
        await ctx.send(board)

def setup(bot):
    bot.add_cog(Games(bot))