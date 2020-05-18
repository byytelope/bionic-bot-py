import discord
from discord.ext import commands

class HelpCommands(commands.Cog):
    """
    Help commands
    """
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def help(self, ctx):

        embed=discord.Embed(
            colour=discord.Colour.blurple(),
            title='Use a "." before command',
            description='How 2 use Aju'
        )
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/592639239683047424/711173474592489543/unknown.png")
        embed.add_field(name='aju', value="Talk to Aju when you're bored.", inline=False)
        embed.add_field(name='corona', value="Use corona confirmed for confirmed and corona deaths for deaths.", inline=False)
        embed.add_field(name='members', value='Aju will count the number of members in the server.', inline=False)
        embed.add_field(name='spam', value="Don't.", inline=False)
        embed.add_field(name='csgo', value='HLTV rankings for all time best CS:GO players.', inline=False)
        embed.add_field(name='clear/cls (Admin role required)', value='Aju will erase a defined number of messages for you. Default value is 3.', inline=False)
        embed.add_field(name='roleid', value="Set message id for role reactions", inline=False)
        embed.set_footer(text='Be nice to Aju thank.')

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(HelpCommands(bot))