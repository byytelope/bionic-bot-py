import discord
from discord.abc import _Undefined
from discord.ext import commands


class AdminCommands(commands.Cog):
    """
    Admin commands for admins
    """

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.inv_author = _Undefined
        self.inv_ch = _Undefined

    @commands.command(aliases=["clear"])
    @commands.has_permissions(manage_messages=True)
    async def cls(self, ctx: commands.Context, amount: int = 2) -> None:
        if amount == 1:
            embed = discord.Embed(
                description=f"cleared `{amount}` message in {ctx.channel.mention}",
                colour=discord.Colour(0xE9ACFD),
            )
        else:
            embed = discord.Embed(
                description=f"cleared `{amount}` messages in {ctx.channel.mention}",
                colour=discord.Colour(0xE9ACFD),
            )
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        result = self.bot.config.find_one({"guild_id": ctx.guild.id, "ch_id_audit": {"$exists": True}})

        if result is None:
            return
        else:
            audit_ch = self.bot.get_channel(result["ch_id_audit"])
            await audit_ch.send(embed=embed)

        await ctx.channel.purge(limit=amount + 1)
        await ctx.channel.send(f"Aju `{amount}` message delete kollin.")

    @commands.command()
    @commands.has_guild_permissions(kick_members=True)
    async def kick(self, ctx: commands.Context, user: discord.Member, *, reason: str = "") -> None:
        embed = discord.Embed(
            title=f"kicked **{user}** from {ctx.guild}.",
            description=reason,
            colour=discord.Colour(0xE9ACFD),
        )
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)

        await user.kick(reason=reason)
        await ctx.send(f"Bye bye {user.mention}.")
        result = self.bot.config.find_one({"guild_id": ctx.guild.id, "ch_id_audit": {"$exists": True}})

        if result is None:
            return
        else:
            audit_ch = self.bot.get_channel(result["ch_id_audit"])
            await audit_ch.send(embed=embed)

    @commands.command(aliases=["reqinv"])
    async def req_invite(self, ctx: commands.Context) -> None:
        self.inv_author = ctx.author
        self.auth_ch = ctx.channel
        result = self.bot.config.find_one({"guild_id": ctx.guild.id, "ch_id_admin": {"$exists": True}})

        if result is None:
            await ctx.send("Please set admin channel first. Use `.set` for more info.")
        else:
            admin_ch = self.bot.get_channel(result["ch_id_admin"])
            await ctx.channel.send("Requesting invite link from admins...")
            await admin_ch.send(
                f"{self.inv_author.mention} is requesting an invite link for {ctx.channel.mention}. Use `.confirm` or `.deny`"
            )

    @commands.command()
    @commands.has_guild_permissions(manage_guild=True)
    async def confirm(self, ctx: commands.Context) -> None:
        link = await ctx.channel.create_invite(max_age=86400, max_uses=2)
        dm = self.bot.get_user(self.inv_author.id)

        embed = discord.Embed(
            title="**confirmed** an invite link request.",
            description=f"from **{self.inv_author}** for {self.auth_ch.mention}",
            colour=discord.Colour(0xE9ACFD),
        )
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)

        await self.auth_ch.send(
            f"Invite link requested by {self.inv_author.mention} was **confirmed**. Pls check your dms for the link."
        )
        await dm.send(f"{link}")

        result = self.bot.config.find_one({"guild_id": ctx.guild.id, "ch_id_audit": {"$exists": True}})

        if result is None:
            return
        else:
            audit_ch = self.bot.get_channel(result["ch_id_audit"])
            await audit_ch.send(embed=embed)

    @commands.command()
    @commands.has_guild_permissions(manage_guild=True)
    async def deny(self, ctx: commands.Context) -> None:
        embed = discord.Embed(
            title="**denied** an invite link request.",
            description=f"from **{self.inv_author}** for {self.auth_ch.mention}",
            colour=discord.Colour(0xE9ACFD),
        )
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)

        await self.auth_ch.send(f"Invite link requested by {self.inv_author.mention} was **denied**.")

        result = self.bot.config.find_one({"guild_id": ctx.guild.id, "ch_id_audit": {"$exists": True}})

        if result is None:
            return
        else:
            audit_ch = self.bot.get_channel(result["ch_id_audit"])
            await audit_ch.send(embed=embed)


def setup(bot) -> None:
    bot.add_cog(AdminCommands(bot))
