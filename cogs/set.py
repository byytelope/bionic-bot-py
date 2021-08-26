import discord
from discord.ext import commands


class Set(commands.Cog):
    """
    Class for setting guild specific vars
    """

    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot

    @commands.group(invoke_without_command=True)
    async def set(self, ctx: commands.Context) -> None:
        embed = discord.Embed(title="set **<command>**", colour=discord.Colour(0xE9ACFD))
        embed.set_footer(text=f"{ctx.guild}", icon_url=f"{ctx.guild.icon_url}")
        embed.add_field(name="rolereactid", value="Set message id for role reactions.", inline=False)
        embed.add_field(
            name="welctextdefault",
            value="Set welcome text for new users. Available variables: \n`{mention}` (mentions member), \n`{user}` (member name without mentioning), \n`{guild}` (name of guild)",
            inline=False,
        )
        embed.add_field(
            name="welctextbots",
            value="Set welcome text for new bots. Available variables: \n`{mention}` (mentions bot), \n`{user}` (bot name without mentioning), \n`{guild}` (name of guild)",
            inline=False,
        )
        embed.add_field(name="welcch", value="Set welcome channel.", inline=False)
        embed.add_field(name="auditch", value="Set audit channel.", inline=False)
        embed.add_field(name="adminch", value="Set admin channel.", inline=False)
        embed.add_field(name="generalch", value="Set general channel.", inline=False)
        embed.add_field(
            name="defaultrole",
            value="Set the default role given to new users.",
            inline=False,
        )
        embed.add_field(
            name="botrole",
            value="Set the default role given to new bots.",
            inline=False,
        )
        embed.set_footer(text=f"Help requested by: {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @set.command(aliases=["rolereactid"])
    @commands.has_guild_permissions(manage_guild=True)
    async def set_msg_id_role(self, ctx: commands.Context, *, msg_id: int) -> None:
        result: dict = self.bot.config.find_one({"guild_id": ctx.guild.id, "msg_id_reaction": {"$exists": True}})
        result_1: dict = self.bot.config.find_one({"guild_id": ctx.guild.id, "ch_id_audit": {"$exists": True}})

        try:
            self.bot.config.update_one(
                {"guild_id": ctx.guild.id},
                {"$set": {"msg_id_reaction": msg_id}},
                upsert=True,
            )
        except Exception as e:
            print(f"Error updating role reaction ID: {e}")
            await ctx.send("Couldn't set role reactions message.")
        else:
            print("Role reaction ID updated.")

            if result is None:
                await ctx.send("Message for role reactions has been set.")
                if result_1 is None:
                    return
                else:
                    audit_ch: discord.TextChannel = self.bot.get_channel(result_1["ch_id_audit"])
                    embed = discord.Embed(
                        description="set the message for role reactions",
                        colour=discord.Colour(0xE9ACFD),
                    )
                    embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                    await audit_ch.send(embed=embed)
            else:
                await ctx.send("Message for role reactions has been changed.")
                if result_1 is None:
                    return
                else:
                    audit_ch = self.bot.get_channel(result_1["ch_id_audit"])

                    embed = discord.Embed(
                        description="changed the message for role reactions",
                        colour=discord.Colour(0xE9ACFD),
                    )
                    embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                    await audit_ch.send(embed=embed)

    @set.command(aliases=["welctextdefault"])
    @commands.has_guild_permissions(manage_guild=True)
    async def set_welc_text_default(self, ctx: commands.Context, *, welc_text: str) -> None:
        result: dict = self.bot.config.find_one({"guild_id": ctx.guild.id, "welc_text_default": {"$exists": True}})
        result_1: dict = self.bot.config.find_one({"guild_id": ctx.guild.id, "ch_id_audit": {"$exists": True}})

        try:
            self.bot.config.update_one(
                {"guild_id": ctx.guild.id},
                {"$set": {"welc_text_default": str(welc_text)}},
                upsert=True,
            )
        except Exception as e:
            print(f"Error updating members welcome text: {e}")
        else:
            print("Members welcome text updated.")

        if result is None:
            await ctx.send(
                f"""
                Welcome text for new users has been set to **"{welc_text}"**
                """
            )
            if result_1 is None:
                return
            else:
                audit_ch: discord.TextChannel = self.bot.get_channel(result_1["ch_id_audit"])
                embed = discord.Embed(
                    description=f'set welcome text for new users to **"{welc_text}"**',
                    colour=discord.Colour(0xE9ACFD),
                )
                embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                await audit_ch.send(embed=embed)
        else:
            await ctx.send(
                f"""
                Welcome text for new users has been changed to "{welc_text}"
                """
            )
            if result_1 is None:
                return
            else:
                audit_ch = self.bot.get_channel(result_1["ch_id_audit"])

                embed = discord.Embed(
                    description=f'changed welcome text for new users to **"{welc_text}"**',
                    colour=discord.Colour(0xE9ACFD),
                )
                embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                await audit_ch.send(embed=embed)

    @set.command(aliases=["welctextbots"])
    @commands.has_guild_permissions(manage_guild=True)
    async def set_welc_text_bots(self, ctx: commands.Context, *, welc_text: str) -> None:
        result: dict = self.bot.config.find_one({"guild_id": ctx.guild.id, "welc_text_bots": {"$exists": True}})
        result_1: dict = self.bot.config.find_one({"guild_id": ctx.guild.id, "ch_id_audit": {"$exists": True}})

        try:
            self.bot.config.update_one(
                {"guild_id": ctx.guild.id},
                {"$set": {"welc_text_bots": str(welc_text)}},
                upsert=True,
            )
        except Exception as e:
            print(f"Error updating bots welcome text: {e}")
        else:
            print("Bots welcome text updated.")

        if result is None:
            await ctx.send(
                f"""
                Welcome text for bots has been set to **"{welc_text}"**
                """
            )
            if result_1 is None:
                return
            else:
                audit_ch: discord.TextChannel = self.bot.get_channel(result_1["ch_id_audit"])
                embed = discord.Embed(
                    description=f'set welcome text for bots to **"{welc_text}"**',
                    colour=discord.Colour(0xE9ACFD),
                )
                embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                await audit_ch.send(embed=embed)
        else:
            await ctx.send(
                f"""
                Welcome text for bots has been changed to "{welc_text}"
                """
            )
            if result_1 is None:
                return
            else:
                audit_ch = self.bot.get_channel(result_1["ch_id_audit"])

                embed = discord.Embed(
                    description=f'changed welcome text for bots to **"{welc_text}"**',
                    colour=discord.Colour(0xE9ACFD),
                )
                embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                await audit_ch.send(embed=embed)

    @set.command(aliases=["welcch"])
    @commands.has_guild_permissions(manage_guild=True)
    async def set_welc_ch(self, ctx: commands.Context, welc_ch: discord.TextChannel) -> None:
        result: dict = self.bot.config.find_one({"guild_id": ctx.guild.id, "ch_id_welcome": {"$exists": True}})
        result_1: dict = self.bot.config.find_one({"guild_id": ctx.guild.id, "ch_id_audit": {"$exists": True}})

        try:
            self.bot.config.update_one(
                {"guild_id": ctx.guild.id},
                {"$set": {"ch_id_welcome": welc_ch.id}},
                upsert=True,
            )
        except Exception as e:
            print(f"Error updating welcome channel ID: {e}")
        else:
            print("Welcome channel ID updated.")

        if result is None:
            await ctx.send(f"Welcome channel has been set to {welc_ch.mention}")
            if result_1 is None:
                return
            else:
                audit_ch: discord.TextChannel = self.bot.get_channel(result_1["ch_id_audit"])
                embed = discord.Embed(
                    description=f"set welcome channel to {welc_ch.mention}",
                    colour=discord.Colour(0xE9ACFD),
                )
                embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                await audit_ch.send(embed=embed)
        else:
            await ctx.send(f"Welcome channel has been changed to {welc_ch.mention}")
            if result_1 is None:
                return
            else:
                audit_ch = self.bot.get_channel(result_1["ch_id_audit"])

                embed = discord.Embed(
                    description=f"changed welcome channel to {welc_ch.mention}",
                    colour=discord.Colour(0xE9ACFD),
                )
                embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                await audit_ch.send(embed=embed)

    @set.command(aliases=["auditch"])
    @commands.has_guild_permissions(manage_guild=True)
    async def set_audit_ch(self, ctx: commands.Context, audit_ch: discord.TextChannel) -> None:
        result: dict = self.bot.config.find_one({"guild_id": ctx.guild.id, "ch_id_audit": {"$exists": True}})

        try:
            self.bot.config.update_one(
                {"guild_id": ctx.guild.id},
                {"$set": {"ch_id_audit": audit_ch.id}},
                upsert=True,
            )
        except Exception as e:
            print(f"Error updating audit channel ID: {e}")
        else:
            print("Audit channel ID updated.")

        if result is None:
            await ctx.send(f"Audit channel has been set to {audit_ch.mention}")
            audit_ch = self.bot.get_channel(result["ch_id_audit"])
            embed = discord.Embed(
                description=f"set audit channel to {audit_ch.mention}",
                colour=discord.Colour(0xE9ACFD),
            )
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
            await audit_ch.send(embed=embed)
        else:
            await ctx.send(f"Audit channel has been changed to {audit_ch.mention}")
            audit_ch = self.bot.get_channel(result["ch_id_audit"])

            embed = discord.Embed(
                description=f"changed audit channel to {audit_ch.mention}",
                colour=discord.Colour(0xE9ACFD),
            )
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
            await audit_ch.send(embed=embed)

    @set.command(aliases=["adminch"])
    @commands.has_guild_permissions(manage_guild=True)
    async def set_admin_ch(self, ctx: commands.Context, admin_ch: discord.TextChannel) -> None:
        result: dict = self.bot.config.find_one({"guild_id": ctx.guild.id, "ch_id_admin": {"$exists": True}})
        result_1: dict = self.bot.config.find_one({"guild_id": ctx.guild.id, "ch_id_audit": {"$exists": True}})

        try:
            self.bot.config.update_one(
                {"guild_id": ctx.guild.id},
                {"$set": {"ch_id_admin": admin_ch.id}},
                upsert=True,
            )
        except Exception as e:
            print(f"Error updating admin channel ID: {e}")
        else:
            print("Admin channel ID updated.")

        if result is None:
            await ctx.send(f"Admin channel has been set to {admin_ch.mention}")
            if result_1 is None:
                return
            else:
                audit_ch: discord.TextChannel = self.bot.get_channel(result_1["ch_id_audit"])
                embed = discord.Embed(
                    description=f"set admin channel to {admin_ch.mention}",
                    colour=discord.Colour(0xE9ACFD),
                )
                embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                await audit_ch.send(embed=embed)
        else:
            await ctx.send(f"Admin channel has been changed to {admin_ch.mention}")
            if result_1 is None:
                return
            else:
                audit_ch = self.bot.get_channel(result_1["ch_id_audit"])

                embed = discord.Embed(
                    description=f"changed admin channel to {admin_ch.mention}",
                    colour=discord.Colour(0xE9ACFD),
                )
                embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                await audit_ch.send(embed=embed)

    @set.command(aliases=["generalch"])
    @commands.has_guild_permissions(manage_guild=True)
    async def set_general_ch(self, ctx: commands.Context, general_ch: discord.TextChannel) -> None:
        result: dict = self.bot.config.find_one({"guild_id": ctx.guild.id, "ch_id_general": {"$exists": True}})
        result_1: dict = self.bot.config.find_one({"guild_id": ctx.guild.id, "ch_id_audit": {"$exists": True}})

        try:
            self.bot.config.update_one(
                {"guild_id": ctx.guild.id},
                {"$set": {"ch_id_general": general_ch.id}},
                upsert=True,
            )
        except Exception as e:
            print(f"Error updating general channel ID: {e}")
        else:
            print("General channel ID updated.")

        if result is None:
            await ctx.send(f"General channel has been set to {general_ch.mention}")
            if result_1 is None:
                return
            else:
                audit_ch: discord.TextChannel = self.bot.get_channel(result_1["ch_id_audit"])
                embed = discord.Embed(
                    description=f"set general channel to {general_ch.mention}",
                    colour=discord.Colour(0xE9ACFD),
                )
                embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                await audit_ch.send(embed=embed)
        else:
            await ctx.send(f"General channel has been changed to {general_ch.mention}")
            if result_1 is None:
                return
            else:
                audit_ch = self.bot.get_channel(result_1["ch_id_audit"])

                embed = discord.Embed(
                    description=f"changed general channel to {general_ch.mention}",
                    colour=discord.Colour(0xE9ACFD),
                )
                embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                await audit_ch.send(embed=embed)

    @set.command(aliases=["defaultrole"])
    @commands.has_guild_permissions(manage_guild=True)
    async def set_role_id_default(self, ctx: commands.Context, default_role: discord.Role) -> None:
        result: dict = self.bot.config.find_one({"guild_id": ctx.guild.id, "role_id_default": {"$exists": True}})
        result_1: dict = self.bot.config.find_one({"guild_id": ctx.guild.id, "ch_id_audit": {"$exists": True}})

        try:
            self.bot.config.update_one(
                {"guild_id": ctx.guild.id},
                {"$set": {"role_id_default": default_role.id}},
                upsert=True,
            )
        except Exception as e:
            print(f"Error updating default role ID: {e}")
        else:
            print("Default role ID updated.")

        if result is None:
            await ctx.send(f"Default role has been set to: {str(default_role)}.")
            if result_1 is None:
                return
            else:
                audit_ch: discord.TextChannel = self.bot.get_channel(result_1["ch_id_audit"])
                embed = discord.Embed(
                    description=f"set default role to: {str(default_role)}",
                    colour=discord.Colour(0xE9ACFD),
                )
                embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                await audit_ch.send(embed=embed)
        else:
            await ctx.send(f"Default role has been changed to: {str(default_role)}")
            if result_1 is None:
                return
            else:
                audit_ch = self.bot.get_channel(result_1["ch_id_audit"])

                embed = discord.Embed(
                    description=f"changed default role to: {str(default_role)}",
                    colour=discord.Colour(0xE9ACFD),
                )
                embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                await audit_ch.send(embed=embed)

    @set.command(aliases=["botrole"])
    @commands.has_guild_permissions(manage_guild=True)
    async def set_role_id_bots(self, ctx: commands.Context, bot_role: discord.Role) -> None:
        result: dict = self.bot.config.find_one({"guild_id": ctx.guild.id, "role_id_bots": {"$exists": True}})
        result_1: dict = self.bot.config.find_one({"guild_id": ctx.guild.id, "ch_id_audit": {"$exists": True}})

        try:
            self.bot.config.update_one(
                {"guild_id": ctx.guild.id},
                {"$set": {"role_id_bots": bot_role.id}},
                upsert=True,
            )
        except Exception as e:
            print(f"Error updating default bot role ID: {e}")
        else:
            print("Default bot role ID updated.")

        if result is None:
            await ctx.send(f"Default role for bots has been set to: {str(bot_role)}.")
            if result_1 is None:
                return
            else:
                audit_ch: discord.TextChannel = self.bot.get_channel(result_1["ch_id_audit"])
                embed = discord.Embed(
                    description=f"set default role for bots to: {str(bot_role)}",
                    colour=discord.Colour(0xE9ACFD),
                )
                embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                await audit_ch.send(embed=embed)
        else:
            await ctx.send(f"Default role for bots has been changed to: {str(bot_role)}")
            if result_1 is None:
                return
            else:
                audit_ch = self.bot.get_channel(result_1["ch_id_audit"])

                embed = discord.Embed(
                    description=f"changed default role for bots to: {str(bot_role)}",
                    colour=discord.Colour(0xE9ACFD),
                )
                embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                await audit_ch.send(embed=embed)


def setup(bot) -> None:
    bot.add_cog(Set(bot))
