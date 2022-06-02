from typing import Union

import discord
import requests
import requests_cache
from discord import app_commands
from discord.ext import commands

session = requests_cache.CachedSession("bot_cache")


class Valorant(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(description="Get your Valorant rank info")
    @app_commands.describe(
        username="Your Valorant username in the format `username#tag`",
        region="The region of your Valorant account",
    )
    @app_commands.choices(
        region=[
            app_commands.Choice(name="Asia Pacific", value="ap"),
            app_commands.Choice(name="Brazil", value="br"),
            app_commands.Choice(name="Europe", value="eu"),
            app_commands.Choice(name="Korea", value="kr"),
            app_commands.Choice(name="Latin America", value="latam"),
            app_commands.Choice(name="North America", value="na"),
        ]
    )
    async def vlrrank(self, interaction: discord.Interaction, username: str, region: str) -> None:
        username_parts = username.split("#")

        mmr_res = requests.get(
            f"https://api.henrikdev.xyz/valorant/v1/mmr/{region}/{username_parts[0]}/{username_parts[1]}"
        )
        mmr_json = mmr_res.json()
        status = mmr_json["status"]

        if status == 403:
            await interaction.response.send_message("Riot server is down for maintenance. Try again.")
        elif status == 404:
            await interaction.response.send_message("Player not found.")
        else:
            mmr_data = mmr_json["data"]
            tiers_res = session.get("https://valorant-api.com/v1/competitivetiers")
            tiers_json = tiers_res.json()
            tiers_data: list[dict[str, Union[str, int, None]]] = tiers_json["data"][-1]["tiers"]
            current_tier_data: dict[str, Union[str, int, None]] = {}

            for tier in tiers_data:
                current_tier_name: str = mmr_data["currenttierpatched"]

                if tier["tierName"] == current_tier_name.upper():
                    current_tier_data = tier

            color = str(current_tier_data["color"])
            color = f"#{color[:len(color) - 2]}"

            embed = (
                discord.Embed(colour=discord.Colour.from_str(color))
                .set_author(
                    name=username,
                    # icon_url="https://seeklogo.com/images/V/valorant-logo-3D72D9117F-seeklogo.com.png",
                    icon_url="attachment://vlr_logo.png",
                )
                .set_thumbnail(url=current_tier_data["largeIcon"])
                .add_field(
                    inline=True,
                    name="Rank",
                    value=mmr_data["currenttierpatched"],
                )
                .add_field(
                    inline=True,
                    name="Progress",
                    value=f"{mmr_data['ranking_in_tier']}/100",
                )
                .set_footer(
                    icon_url=interaction.user.display_avatar.url,
                    text=f"requested by: {interaction.user}",
                )
            )
            file = discord.File("assets/vlr_logo.png", filename="vlr_logo.png")

            await interaction.response.send_message(file=file, embed=embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Valorant(bot))
