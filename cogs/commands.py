import random
import sys
import os

import discord
from discord import app_commands
from discord.ext import commands


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from bot import BionicBot


class Commands(commands.Cog):
    def __init__(self, bot: BionicBot) -> None:
        self.bot = bot

    @app_commands.command(description="Check latency")
    async def ping(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_message(
            f"🏓 {round(self.bot.latency * 1000)} ms."
        )

    @app_commands.command(description="Get to know BionicBot")
    async def help(self, interaction: discord.Interaction) -> None:
        info = await self.bot.application_info()
        bot_avatar_url = (
            self.bot.user.display_avatar.url if self.bot.user != None else ""
        )

        embed = (
            discord.Embed(
                title="Hello, I am BionicBot",
                description="Press `/` and you can browse through all my commands and their descriptions.",
                colour=discord.Colour.from_rgb(117, 251, 147),
            )
            .set_footer(
                icon_url=info.owner.display_avatar.url,
                text=f"Bot made by: {info.owner}",
            )
            .set_thumbnail(url=bot_avatar_url)
        )

        await interaction.response.send_message(embed=embed)

    @app_commands.command(description="Make BionicBot say whatever you want")
    async def say(self, interaction: discord.Interaction, text: str) -> None:
        randomness = [random.randint(0, 1) for _ in range(len(text))]
        funnied = "".join(
            [
                text[i].upper() if rand == 1 else text[i].lower()
                for i, rand in enumerate(randomness)
            ]
        )
        await interaction.response.send_message(funnied)

    @app_commands.command(description="Get activity status")
    async def activity(
        self, interaction: discord.Interaction, member: discord.Member
    ) -> None:
        current_member = member.guild.get_member(member.id)

        assert current_member != None
        if current_member.activities[0]:
            assert current_member.activities[0].name != None
            await interaction.response.send_message(current_member.activities[0].name)
        else:
            await interaction.response.send_message(
                f"{current_member} is currently not doing anything."
            )


async def setup(bot: BionicBot) -> None:
    await bot.add_cog(Commands(bot))
