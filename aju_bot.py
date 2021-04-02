import os
import random

import discord
from discord.ext import commands
from pymongo import MongoClient


intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix=commands.when_mentioned_or("."), intents=intents, owner_id=367686193242177536)
bot.remove_command("help")


@bot.event
async def on_ready() -> None:
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("use .help for help"))
    try:
        mongo = MongoClient(os.environ["AJU_MONGO_URI"])
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
    bot.db = mongo["aju_bot_db"]
    bot.config = bot.db["guild_config"]
    print("Aju is ready.")


@bot.event
async def on_message(message) -> None:
    if bot.user.mentioned_in(message):
        prefix = await bot.get_prefix(message)
        await message.channel.send(f"Type {prefix[-1]}help for help.")
    await bot.process_commands(message)


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
        responses = ["They aju ah niegey command ah.", "Aju ah egey ehthakaau keyfele."]
        await ctx.send(random.choice(responses))


@bot.event
async def on_cls_error(ctx, error) -> None:
    if isinstance(error, (commands.MissingPermissions, commands.MissingAnyRole)):
        responses = [
            "Adhi the command beynun vey varah ekalo bondo nivei.",
            "Hoho kanthethi.",
            "Nononono.",
            "U cannot la.",
        ]
        await ctx.send(random.choice(responses))


cogs: list[str] = [
    "cogs.admin",
    "cogs.funny",
    "cogs.help",
    "cogs.image_downloader",
    "cogs.music",
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

bot.run(os.environ["AJU_API_KEY"])
