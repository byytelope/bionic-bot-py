import sys
import os

import discord
from discord import app_commands
from discord.ext import commands


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from bot import BionicBot

# TEST
# MY_GUILD = discord.Object(id=835682783338561549)

# BIONIC
MY_GUILD = discord.Object(id=585576337041784862)


class Admin(commands.Cog):
    def __init__(self, bot: BionicBot) -> None:
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def sync(self, ctx: commands.Context[BionicBot]) -> None:
        self.bot.tree.copy_global_to(guild=MY_GUILD)
        await self.bot.tree.sync(guild=MY_GUILD)
        await ctx.send("App commands successfully synced. ✅")

    @app_commands.command(
        description="Delete specified number of messages from channel"
    )
    @app_commands.describe(amount="Number of messasges to delete, default is 1")
    async def cls(self, interaction: discord.Interaction, amount: int = 1) -> None:
        ch = interaction.channel
        assert ch != None and ch.type == discord.ChannelType.text

        await ch.purge(limit=amount)  # type: ignore
        await interaction.response.send_message(
            f"{interaction.user.mention} deleted `{amount}` message{'s' if amount > 1 else ''}."
        )

    @app_commands.command(description="Set welcome channel")
    @app_commands.describe(channel="A Discord text channel")
    async def set_welc_ch(
        self, interaction: discord.Interaction, channel: discord.TextChannel
    ) -> None:

        guild_config = self.bot.db.guild_config.find_one({"id": interaction.guild_id})

        if guild_config == None:
            self.bot.db.guild_config.insert_one(
                {"id": interaction.guild_id, "ch_id_welcome": channel.id}
            )

        await interaction.response.send_message(
            f"Set {channel.mention} as welcome channel."
        )

    @app_commands.command(description="Set default role")
    @app_commands.describe(
        channel="Set role that is automatically assigned to new members"
    )
    async def set_default_role(
        self, interaction: discord.Interaction, role: discord.Role
    ) -> None:

        guild_config = self.bot.db.guild_config.find_one({"id": interaction.guild_id})

        if guild_config == None:
            self.bot.db.guild_config.insert_one(
                {"id": interaction.guild_id, "role_id_default": role.id}
            )

        await interaction.response.send_message(f"Set {role} as default role.")

    @sync.error
    async def sync_error(
        self, ctx: commands.Context[BionicBot], error: commands.CommandError
    ) -> None:
        if isinstance(error, commands.NotOwner):
            app_info = await self.bot.application_info()
            await ctx.send(
                f"Only {app_info.owner.mention} is allowed to use this command."
            )


async def setup(bot: BionicBot) -> None:
    await bot.add_cog(Admin(bot))
