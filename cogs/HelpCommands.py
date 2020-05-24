import discord
import os
import psycopg2
from discord.ext import commands

class HelpCommands(commands.Cog):
    """
    Help commands
    """
    def __init__(self, bot):
        self.bot = bot

        db_database = os.environ['db_database']
        db_user = os.environ['db_user']
        db_password = os.environ['db_password']
        db_host = os.environ['db_host']
        db_port = os.environ['db_port']

        self.db = psycopg2.connect(
            database=db_database, 
            user=db_user, 
            password=db_password, 
            host=db_host, 
            port=db_port
            )
        self.cursor = self.db.cursor()
    
    @commands.group(invoke_without_command=True)
    async def help(self, ctx):

        embed=discord.Embed(
            title='Hello am Aju',
            description='Use **.help** and a command from below for more info.',
            colour=discord.Colour.blurple()
        )
        embed.set_author(name='Aju', icon_url='https://cdn.discordapp.com/attachments/592639239683047424/711173474592489543/unknown.png')
        embed.add_field(name='aju', value="Talk to Aju when you're bored.", inline=False)
        embed.add_field(name='corona', value="Get realtime corona stats.", inline=False)
        embed.add_field(name='members', value='Aju counts the number of members in your server.', inline=False)
        embed.add_field(name='spam', value="Don't.", inline=False)
        embed.add_field(name='csgo', value='HLTV rankings for all time best CS:GO players.', inline=False)
        embed.add_field(name='reqinv', value='Request an invite link.', inline=False)
        embed.add_field(name='clear/cls (Admin role required)', value='Clear messages from a channel.', inline=False)
        embed.add_field(name='set (cannot be used with .help)', value='Use .set for info on setting variables for your server.', inline=False)
        embed.set_footer(text=f'Help requested by: {ctx.author.name}')

        await ctx.send(embed=embed)

    @help.command(aliases=['aju'])
    async def help_aju(self, ctx):
        embed=discord.Embed(
            colour=discord.Colour.blurple(),
            title='Talk to Aju',
            description='Use **.aju** and say anything.'
        )
        await ctx.send(embed=embed)

    @help.command(aliases=['corona'])
    async def help_corona(self, ctx):
        embed=discord.Embed(
            colour=discord.Colour.blurple(),
            title='Get realtime corona stats',
            description='Use **.corona** and **confirmed** for the  number of confirmed cases or **deaths** for the  number of confirmed deaths.'
        )
        await ctx.send(embed=embed)

    @help.command(aliases=['members'])
    async def help_members(self, ctx):
        embed=discord.Embed(
            colour=discord.Colour.blurple(),
            title='Get the total number of members in your guild',
            description='Pretty self explanatory.'
        )
        await ctx.send(embed=embed)

    @help.command(aliases=['spam'])
    async def help_spam(self, ctx):

        self.cursor.execute(f"SELECT ch_id_general FROM main WHERE guild_id = ('{str(ctx.guild.id)}')")
        result_1 = self.cursor.fetchone()
        if result_1 is None:
            embed=discord.Embed(
                colour=discord.Colour.blurple(),
                title='No.',
                description='Will not work in general.'
            )
        else:
            general_ch = self.bot.get_channel(id=int(result_1[0]))
            embed=discord.Embed(
                colour=discord.Colour.blurple(),
                title='No.',
                description=f'Will not work in {general_ch.mention}.'
            )
        
        await ctx.send(embed=embed)

    @help.command(aliases=['csgo'])
    async def help_csgo(self, ctx):
        embed=discord.Embed(
            colour=discord.Colour.blurple(),
            title='ZyWoah',
            description='Use **.csgo** and then a number (eg: .csgo 1 for the number 1 position).'
        )
        await ctx.send(embed=embed)

    @help.command(aliases=['reqinv'])
    async def help_reqinv(self, ctx):
        embed=discord.Embed(
            colour=discord.Colour.blurple(),
            title='Request an invite link from the admins.',
            description='.reqinv will send a request for an invite link to the admin channel of the guild. Only works if admin channel is setup in Aju.'
        )
        await ctx.send(embed=embed)

    @help.command(aliases=['cls', 'clear'])
    async def help_cls(self, ctx):
        embed=discord.Embed(
            colour=discord.Colour.blurple(),
            title='Clear the bs',
            description='Use **.cls** or **.clear** followed by a number to clear texts. If not specified, 2 texts will be cleared.'
        )
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(HelpCommands(bot))