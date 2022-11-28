import os
import sys
from typing import Union

import discord
import requests
import requests_cache
from discord import app_commands
from discord.ext import commands

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from bot import BionicBot

session = requests_cache.CachedSession("bot_cache")


class Valorant(commands.Cog):
    def __init__(self, bot: BionicBot) -> None:
        self.bot = bot
        self.bot.tree.on_error = self.on_err

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
    async def vlrrank(
        self,
        interaction: discord.Interaction,
        username: str,
        region: app_commands.Choice[str],
    ) -> None:
        username_parts = username.split("#")

        mmr_res = requests.get(
            f"https://api.henrikdev.xyz/valorant/v1/mmr/{region.value}/{username_parts[0]}/{username_parts[1]}"
        )
        mmr_json = mmr_res.json()
        status = mmr_json["status"]

        if status == 403:
            await interaction.response.send_message(
                "Riot server is down for maintenance. Try again."
            )
        elif status == 404:
            await interaction.response.send_message("Player not found.")
        else:
            mmr_data = mmr_json["data"]
            tiers_res = session.get("https://valorant-api.com/v1/competitivetiers")
            tiers_json = tiers_res.json()
            tiers_data: list[dict[str, Union[str, int, None]]] = tiers_json["data"][-1][
                "tiers"
            ]
            current_tier_data: dict[str, Union[str, int, None]] = {}
            rank_name: str = (
                mmr_data["currenttierpatched"]
                if mmr_data["currenttierpatched"] != None
                else "UNRANKED"
            )
            rank_progress = (
                mmr_data["ranking_in_tier"]
                if mmr_data["ranking_in_tier"] != None
                else "??"
            )

            for tier in tiers_data:
                if tier["tierName"] == rank_name.upper():
                    current_tier_data = tier

            color = str(current_tier_data["color"])
            color = f"#{color[:len(color) - 2]}"

            embed = (
                discord.Embed(colour=discord.Colour.from_str(color))
                .set_author(
                    name=username,
                    icon_url="attachment://vlr_logo.png",
                )
                .set_thumbnail(url=current_tier_data["largeIcon"])
                .add_field(
                    inline=True,
                    name="Rank",
                    value=rank_name,
                )
                .add_field(
                    inline=True,
                    name="Progress",
                    value=f"{rank_progress}/100",
                )
                .set_footer(
                    icon_url=interaction.user.display_avatar.url,
                    text=f"requested by: {interaction.user}",
                )
            )
            file = discord.File("assets/vlr_logo.png", filename="vlr_logo.png")

            await interaction.response.send_message(file=file, embed=embed)

    @staticmethod
    async def on_err(
        interaction: discord.Interaction, error: app_commands.AppCommandError
    ) -> None:
        print(f"Error: {error}")


async def setup(bot: BionicBot) -> None:
    await bot.add_cog(Valorant(bot))
