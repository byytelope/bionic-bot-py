import random
from typing import List

import discord
import requests
from covid import Covid
from discord.ext import commands
from utils.web_scraper import web_scrape

covid = Covid()


class Stats(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command()
    async def ping(self, ctx: commands.Context) -> None:
        await ctx.send(f"{round(self.bot.latency * 1000)}ms in thiyaa aju ah libenei.")

    @commands.command()
    async def members(self, ctx: commands.Context) -> None:
        await ctx.send(f"There are `{ctx.guild.member_count}` **hopefully** corona-free people in {ctx.guild}.")

    @commands.command(name="csgo")
    async def aju_csgo(self, ctx: commands.Context, num: int) -> None:
        await ctx.send(web_scrape(num - 1))

    @commands.command(aliases=["covid"])
    async def corona(self, ctx: commands.Context, country: str, args: str) -> None:
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
        elif country.lower() == "usa" or country.lower() == "us":
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
    async def on_corona_error(self, ctx: commands.Context, error: commands.CommandError) -> None:
        if isinstance(error, (commands.MissingRequiredArgument, commands.UserInputError)):
            responses = [
                "Corona cowcow?",
                "Adhi ada neevene ey.",
                "Thankeda baaraa benafele.",
                "Corona wot?",
                "Thehen ekani benagen keraah vee kamah aju ah egei?",
            ]
            await ctx.send(random.choice(responses))

    @commands.command(name="vlrrank")
    async def vlr_rank(self, ctx: commands.Context, username: str, region: str) -> None:
        await ctx.send("Fetching your Valorant MMR...", delete_after=0)

        username_lst = username.split("#")
        url = f"https://api.henrikdev.xyz/valorant/v1/mmr/{region}/{username_lst[0]}/{username_lst[1]}"
        res = requests.get(url).json()

        if res["status"] == "200":
            rank: str = res["data"]["currenttierpatched"]
            rank_lower = rank.replace(" ", "").lower()
            embed_color = discord.Colour.from_rgb(255, 70, 84)

            if "iron" in rank_lower:
                embed_color = discord.Colour.from_rgb(86, 88, 86)
            elif "bronze" in rank_lower:
                embed_color = discord.Colour.from_rgb(130, 93, 29)
            elif "silver" in rank_lower:
                embed_color = discord.Colour.from_rgb(200, 206, 206)
            elif "gold" in rank_lower:
                embed_color = discord.Colour.from_rgb(228, 199, 98)
            elif "platinum" in rank_lower:
                embed_color = discord.Colour.from_rgb(119, 208, 220)
            elif "diamond" in rank_lower:
                embed_color = discord.Colour.from_rgb(226, 154, 237)
            elif "immortal" in rank_lower:
                embed_color = discord.Colour.from_rgb(161, 51, 61)
            elif "radiant" in rank_lower:
                embed_color = discord.Colour.from_rgb(245, 245, 230)

            embed = discord.Embed(
                description=f"**{res['data']['name']}**#{res['data']['tag']}",
                colour=embed_color,
            )

            file = discord.File(f"assets/ranks/{rank_lower}.png", filename=f"{rank_lower}.png")

            embed.set_thumbnail(url=f"attachment://{rank_lower}.png")
            embed.set_footer(text=f"Requested by: {ctx.author}", icon_url=ctx.author.avatar_url)
            embed.add_field(name="Rank", value=res["data"]["currenttierpatched"])
            embed.add_field(name="Elo", value=res["data"]["elo"])

            await ctx.send(embed=embed, file=file)
        else:
            await ctx.send(res["message"])

    @vlr_rank.error
    async def on_vlr_rank_error(self, ctx: commands.Context, error: commands.CommandError) -> None:
        if isinstance(error, (commands.MissingRequiredArgument, commands.UserInputError)):
            await ctx.send("Provide a valid user with # tag and the region.")

    @commands.command(aliases=["vlrleaderboard", "vlrlb"])
    async def vlr_leaderboard(self, ctx: commands.Context, region: str = "ap"):
        await ctx.send("Fetching Valorant leaderboard...", delete_after=0)

        url = f"https://api.henrikdev.xyz/valorant/v1/leaderboard/{region}"
        res: List[dict] = requests.get(url).json()
        top_10_lst = res[:10]
        top_10_str = ""
        ranks = ""

        embed = discord.Embed(
            title=f"Valorant {region.upper()} Top 10",
            colour=discord.Colour.from_rgb(255, 70, 84),
        )

        file = discord.File("assets/vlrlogo.png", filename="vlrlogo.png")

        embed.set_thumbnail(url="attachment://vlrlogo.png")
        embed.set_footer(text=f"Requested by: {ctx.author}", icon_url=ctx.author.avatar_url)

        for i, player in enumerate(top_10_lst):
            player_name: str = ""

            if player["gameName"] != "":
                player_name = f"**{player['gameName']}**" + "#" + player["tagLine"]
            else:
                player_name = "**-Anon-**"

            top_10_str += player_name + "\n\n"
            ranks += str(i+1) + "\n\n"

        embed.add_field(name="Rank", value=ranks)
        embed.add_field(name="Player", value=top_10_str)

        await ctx.send(embed=embed, file=file)


def setup(bot) -> None:
    bot.add_cog(Stats(bot))
