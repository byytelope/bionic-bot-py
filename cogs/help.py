import os

import discord
import psycopg2
from discord.ext import commands


class HelpCommands(commands.Cog):
    """
    Help commands
    """

    def __init__(self, bot: commands.Bot):
        self.bot = bot

        db_database = os.environ["AJU_DB_DATABASE"]
        db_user = os.environ["AJU_DB_USER"]
        db_password = os.environ["AJU_DB_PASSWORD"]
        db_host = os.environ["AJU_DB_HOST"]
        db_port = os.environ["AJU_DB_PORT"]

        try:
            self.db = psycopg2.connect(
                database=db_database,
                user=db_user,
                password=db_password,
                host=db_host,
                port=db_port,
            )
        except psycopg2.OperationalError as e:
            print(e)

        self.cursor = self.db.cursor()

    @commands.group(invoke_without_command=True)
    async def help(self, ctx: commands.Context):

        embed = discord.Embed(
            title="Hello am Aju",
            description="Use `.help` and a command from below for more info.",
            colour=discord.Colour(0xE9ACFD),
        )
        embed.add_field(name="aju", value="Talk to Aju when you're bored.", inline=False)
        embed.add_field(name="say", value="MaKe ajU say AnYThinG.", inline=False)
        embed.add_field(name="corona", value="Get realtime corona stats.", inline=False)
        embed.add_field(
            name="members",
            value="Aju counts the number of members in your server.",
            inline=False,
        )
        embed.add_field(name="spam", value="Don't.", inline=False)
        embed.add_field(
            name="csgo",
            value="HLTV rankings for all time best CS:GO players.",
            inline=False,
        )
        embed.add_field(name="reqinv", value="Request an invite link.", inline=False)
        embed.add_field(name="avatar", value="Get a user's avatar.", inline=False)
        embed.add_field(name="img", value="Search Google for images.", inline=False)
        embed.add_field(name="gif", value="Search Google for gifs.", inline=False)
        embed.add_field(
            name="clear/cls **(Admin role required)**",
            value="Clear messages from a channel.",
            inline=False,
        )
        embed.add_field(
            name="set **(cannot be used with .help)**",
            value="Use `.set` for info on setting variables for your server.",
            inline=False,
        )
        embed.set_footer(text=f"Help requested by: {ctx.author}", icon_url=ctx.author.avatar_url)

        await ctx.send(embed=embed)

    @help.command(aliases=["aju"])
    async def help_aju(self, ctx: commands.Context):
        embed = discord.Embed(
            colour=discord.Colour(0xE9ACFD),
            title="Talk to Aju",
            description="Use `.aju` and say anything.",
        )
        embed.set_footer(text=f"Help requested by: {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @help.command(aliases=["say"])
    async def help_say(self, ctx: commands.Context):
        embed = discord.Embed(
            colour=discord.Colour(0xE9ACFD),
            title="@eCho On",
            description="Use `.say` and Aju will RePEaT aNYTHINg AFtEr the coMmAnd.",
        )
        embed.set_footer(text=f"Help requested by: {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @help.command(aliases=["corona"])
    async def help_corona(self, ctx: commands.Context):
        embed = discord.Embed(
            colour=discord.Colour(0xE9ACFD),
            title="Get realtime corona stats",
            description="Use `.corona global confirmed` for total confirmed cases globally. You can substitute in `deaths`, `recovered` and `active` instead of `confirmed` and any country in place of `global`.",
        )
        embed.set_footer(text=f"Help requested by: {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @help.command(aliases=["members"])
    async def help_members(self, ctx: commands.Context):
        embed = discord.Embed(
            colour=discord.Colour(0xE9ACFD),
            title="Get the total number of members in your guild",
            description="Pretty self explanatory.",
        )
        embed.set_footer(text=f"Help requested by: {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @help.command(aliases=["spam"])
    async def help_spam(self, ctx: commands.Context):

        self.cursor.execute(f"SELECT ch_id_general FROM main WHERE guild_id = ('{str(ctx.guild.id)}')")
        result_1 = self.cursor.fetchone()
        if result_1 is None:
            embed = discord.Embed(
                colour=discord.Colour(0xE9ACFD),
                title="No.",
                description="Will not work in the general channel.",
            )
        else:
            general_ch = self.bot.get_channel(id=int(result_1[0]))
            embed = discord.Embed(
                colour=discord.Colour(0xE9ACFD),
                title="No.",
                description=f"Will not work in {general_ch.mention}.",
            )
        embed.set_footer(text=f"Help requested by: {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @help.command(aliases=["csgo"])
    async def help_csgo(self, ctx: commands.Context):
        embed = discord.Embed(
            colour=discord.Colour(0xE9ACFD),
            title="ZyWoah",
            description="Use `.csgo` and then a number (eg: `.csgo 1` for the number 1 position).",
        )
        embed.set_footer(text=f"Help requested by: {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @help.command(aliases=["reqinv"])
    async def help_reqinv(self, ctx: commands.Context):
        embed = discord.Embed(
            colour=discord.Colour(0xE9ACFD),
            title="Request an invite link from the admins.",
            description="`.reqinv` will send a request for an invite link to the admin channel of the guild. Only works if admin channel is setup in Aju.",
        )
        embed.set_footer(text=f"Help requested by: {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @help.command(aliases=["avatar"])
    async def help_avatar(self, ctx: commands.Context):
        embed = discord.Embed(
            colour=discord.Colour(0xE9ACFD),
            title="Get the avatar of a user.",
            description="Use `.avatar *userID, server nickname or mention*` to get avatar.",
        )
        embed.set_footer(text=f"Help requested by: {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @help.command(aliases=["img"])
    async def help_img(self, ctx: commands.Context):
        embed = discord.Embed(
            colour=discord.Colour(0xE9ACFD),
            title="Search for an image on Google.",
            description="Use `.img` followed by a search term. eg: `.img funny vine compilation`",
        )
        embed.set_footer(text=f"Help requested by: {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @help.command(aliases=["gif"])
    async def help_gif(self, ctx: commands.Context):
        embed = discord.Embed(
            colour=discord.Colour(0xE9ACFD),
            title="Search for a gif on Google.",
            description="Use `.gif` followed by a search term. eg: `.gif funny lele pons vines` **may take ~ a minute to send sometimes**",
        )
        embed.set_footer(text=f"Help requested by: {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @help.command(aliases=["cls", "clear"])
    async def help_cls(self, ctx: commands.Context):
        embed = discord.Embed(
            colour=discord.Colour.blurple(),
            title="Clear the bs",
            description="Use `.cls` or `.clear` followed by a number to clear texts. If not specified, 2 texts will be cleared.",
        )
        embed.set_footer(text=f"Help requested by: {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(HelpCommands(bot))
