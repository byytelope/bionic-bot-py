import discord
from discord.ext import commands


class Welcome(commands.Cog):
    """
    Welcome actions
    """

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member) -> None:
        result = self.bot.config.find_one({"guild_id": member.guild.id, "role_id_default": {"$exists": True}})
        result_1 = self.bot.config.find_one({"guild_id": member.guild.id, "ch_id_welcome": {"$exists": True}})
        result_2 = self.bot.config.find_one({"guild_id": member.guild.id, "welc_text": {"$exists": True}})

        if result is None:
            return
        else:
            default_role = discord.utils.get(iterable=member.guild.roles, id=result["role_id_default"])
            await member.add_roles(default_role)
            print(f"{member} was given {default_role}")

        if result_1 is None:
            return
        else:
            welc_ch = self.bot.get_channel(result_1["ch_id_welcome"])
            msg: str = result_2["welc_text"] or "Hope you enjoy your stay {member}!"

            embed = discord.Embed(
                title=f"Welcome to {member.guild}!",
                description=msg.format(mention=member.mention, user=member.name, guild=member.guild),
                colour=discord.Colour(0xE9ACFD),
            )
            embed.set_thumbnail(url=member.avatar_url)
            embed.set_footer(text=member.guild, icon_url=member.guild.icon_url)
            await welc_ch.send(embed=embed)


def setup(bot) -> None:
    bot.add_cog(Welcome(bot))