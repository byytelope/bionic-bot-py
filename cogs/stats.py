import random
import sys
from os import path

from covid import Covid
from discord.ext import commands

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from not_cogs.web_scraper import web_scrape

covid = Covid()


class Stats(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f"{round(self.bot.latency * 1000)}ms in thiyaa aju ah libenei.")

    @commands.command()
    async def members(self, ctx: commands.Context):
        await ctx.send(f"There are `{ctx.guild.member_count}` **hopefully** corona-free people in {ctx.guild}.")

    @commands.command(name="csgo")
    async def aju_csgo(self, ctx: commands.Context, num: int):
        await ctx.send(web_scrape(num - 1))

    @commands.command()
    async def corona(self, ctx: commands.Context, country: str, args: str):
        if country.lower() == "global" and args == "confirmed":
            result = covid.get_total_confirmed_cases()
        elif country.lower() == "global" and args == "active":
            result = covid.get_total_active_cases()
        elif country.lower() == "global" and args == "deaths":
            result = covid.get_total_deaths()
        elif country.lower() == "global" and args == "recovered":
            result = covid.get_total_recovered()
        elif country.lower() == "mv":
            result = covid.get_status_by_country_name("Maldives")[args.lower()]
        elif country.lower() == "usa":
            result = covid.get_status_by_country_name("US")[args.lower()]
        else:
            country_name = []
            countries = covid.list_countries()
            for c in countries:
                name = c["name"]
                if country in name.lower():
                    country_name.append(name)
            if len(country_name) == 0:
                result = None
            else:
                result = covid.get_status_by_country_name(country_name[0])[args.lower()]
        if not result:
            stmts = ["Aju ah the gaumu nifenene.", "Adhi niegene.", "They konthaan?", "Hadhaganfe thehen key gaumah."]
            stmt = random.choice(stmts)
        else:
            if result <= 10:
                stmt = f"{result:,d} thakah meehun."
            else:
                stmt = f"{result:,d} hei meehun."
        await ctx.send(stmt)

    @corona.error
    async def on_corona_error(self, ctx: commands.Context, error: commands.errors):
        if isinstance(error, (commands.MissingRequiredArgument, commands.UserInputError)):
            responses = [
                "Corona cowcow?",
                "Adhi ada neevene ey.",
                "Thankeda baaraa benafele.",
                "Corona wot?",
                "Thehen ekani benagen keraah vee kamah aju ah egei?",
            ]
            await ctx.send(random.choice(responses))


def setup(bot):
    bot.add_cog(Stats(bot))
