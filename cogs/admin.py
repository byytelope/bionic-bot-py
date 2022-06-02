import discord
from discord import app_commands
from discord.ext import commands

# MY_GUILD = discord.Object(id=835682783338561549)
MY_GUILD = discord.Object(id=585576337041784862)


class Admin(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def sync(self, ctx: commands.Context[commands.Bot]) -> None:
        self.bot.tree.copy_global_to(guild=MY_GUILD)
        await self.bot.tree.sync(guild=MY_GUILD)
        await ctx.send("App commands successfully synced. ✅")

    @app_commands.command(description="Delete specified number of messages from channel")
    @app_commands.describe(amount="Number of messasges to delete, default is 1")
    async def cls(self, interaction: discord.Interaction, amount: int = 1) -> None:
        assert interaction.channel != None

        if interaction.channel.type == discord.ChannelType.text:
            await interaction.channel.purge(limit=amount)  # type: ignore

        await interaction.response.send_message(
            f"{interaction.user.mention} deleted `{amount}` message{'s' if amount > 1 else ''}."
        )

    @sync.error
    async def sync_error(self, ctx: commands.Context[commands.Bot], error: commands.CommandError) -> None:
        if isinstance(error, commands.NotOwner):
            app_info = await self.bot.application_info()
            await ctx.send(f"Only {app_info.owner.mention} is allowed to use this command.")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Admin(bot))
