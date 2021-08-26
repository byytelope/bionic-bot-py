import discord
from discord.ext import commands


class Roles(commands.Cog):
    """
    Reaction roles and init role
    """

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent) -> None:
        message_id = payload.message_id
        result = self.bot.config.find_one({"guild_id": payload.guild_id, "msg_id_reaction": {"$exists": True}})

        if message_id == result["msg_id_reaction"]:
            guild_id = payload.guild_id
            guild: discord.Guild = discord.utils.find(lambda f: f.id == guild_id, self.bot.guilds)
            role = discord.utils.get(iterable=guild.roles, name=payload.emoji.name)

            if role is not None:
                member = discord.utils.find(lambda ree: ree.id == payload.user_id, guild.members)
                if member is not None:
                    await member.add_roles(role)
                    print(f"Added {role} to {member}")
                else:
                    print("Member not found.")
            else:
                print("Role not found.")

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent) -> None:
        message_id = payload.message_id
        result = self.bot.config.find_one({"guild_id": payload.guild_id, "msg_id_reaction": {"$exists": True}})

        if message_id == result["msg_id_reaction"]:
            guild_id = payload.guild_id
            guild: discord.Guild = discord.utils.find(lambda bruh: bruh.id == guild_id, self.bot.guilds)
            role = discord.utils.get(iterable=guild.roles, name=payload.emoji.name)

            if role is not None:
                member = discord.utils.find(lambda ree: ree.id == payload.user_id, guild.members)
                if member is not None:
                    await member.remove_roles(role)
                    print(f"Removed {role} from {member}")
                else:
                    print("Member not found.")
            else:
                print("Role not found.")


def setup(bot) -> None:
    bot.add_cog(Roles(bot))
