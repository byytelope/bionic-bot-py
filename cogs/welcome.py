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
        print(member.bot)
        result = self.bot.config.find_one({"guild_id": member.guild.id, "role_id_default": {"$exists": True}})
        result_1 = self.bot.config.find_one({"guild_id": member.guild.id, "role_id_bots": {"$exists": True}})
        result_2 = self.bot.config.find_one({"guild_id": member.guild.id, "ch_id_welcome": {"$exists": True}})
        result_3 = self.bot.config.find_one({"guild_id": member.guild.id, "welc_text_default": {"$exists": True}})

        if result is None:
            return
        elif not member.bot:
            default_role = discord.utils.get(iterable=member.guild.roles, id=result["role_id_default"])
            await member.add_roles(default_role)
            print(f"New member {member} was given {default_role}")

        if result_1 is None:
            return
        elif member.bot:
            bots_role = discord.utils.get(iterable=member.guild.roles, id=result_1["role_id_bots"])
            await member.add_roles(bots_role)
            print(f"New bot {member} was given {bots_role}")

        if result_2 is None:
            return
        else:
            welc_ch = self.bot.get_channel(result_2["ch_id_welcome"])
            if member.bot:
                msg = result_3.get("welc_text_bots") or "Say hello to {mention}!"
            else:
                msg = result_3.get("welc_text_default") or "Hope you enjoy your stay {mention}!"

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