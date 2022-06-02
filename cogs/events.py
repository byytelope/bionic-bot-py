from discord.ext import commands


class Events(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        print(f"\nLogged in as: {self.bot.user}")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Events(bot))
