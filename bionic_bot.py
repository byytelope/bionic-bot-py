import logging
import os
import random

import discord
from discord.ext import commands
from pymongo import MongoClient

logger = logging.getLogger("discord")
logger.setLevel(logging.DEBUG)

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix=commands.when_mentioned_or("."), intents=intents, owner_id=367686193242177536)
bot.remove_command("help")

@bot.event
async def on_ready() -> None:
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("use .help for help"))

    try:
        mongo = MongoClient(os.environ["BIONIC_MONGO_URI"])
        bot.db = mongo["bionic_bot_db"] # type: ignore
        bot.config = bot.db["guild_config"] # type: ignore
    except Exception as e:
        mongo = None
        print(f"Error connecting to MongoDB: {e}")

    print("Bot is ready.")

@bot.command(
    aliases=[
        ".",
        "..",
        "...",
        "....",
        ".....",
        "......",
        ".......",
        "........",
        ".........",
        "..........",
    ]
)
async def ignore() -> None:
    try:
        pass
    except Exception:
        pass


@bot.event
async def on_command_error(ctx, error) -> None:
    if isinstance(error, commands.CommandNotFound):
        responses = ["They mah ah niegey command ah.", "Mah egey ehthakaau keyfele."]
        await ctx.send(random.choice(responses))


cogs: list[str] = [
    "cogs.admin",
    "cogs.funny",
    "cogs.help",
    "cogs.image_downloader",
    "cogs.roles",
    "cogs.set",
    "cogs.stats",
    "cogs.welcome",
]

if __name__ == "__main__":
    for cog in cogs:
        try:
            bot.load_extension(cog)
            print(f"{cog.replace('cogs.', '')} loaded successfully.")
        except Exception as cog_error:
            print(f"Couldn't load {cog.replace('cogs.', '')}\n")
            print(cog_error)

bot.run(os.environ["BIONIC_API_KEY"])
