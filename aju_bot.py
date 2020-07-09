import os
import random
import discord
import psycopg2
from discord.ext import commands
from web_scraper import web_scrape

bot = commands.Bot(command_prefix=".", owner_id=367686193242177536)
bot.remove_command("help")


@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("use .help for help"))

    db_database = os.environ["db_database"]
    db_user = os.environ["db_user"]
    db_password = os.environ["db_password"]
    db_host = os.environ["db_host"]
    db_port = os.environ["db_port"]

    try:
        db = psycopg2.connect(database=db_database, user=db_user, password=db_password, host=db_host, port=db_port,)
        print("Successfully connected to database.")
    except psycopg2.OperationalError as db_error:
        print(db_error)
        print("Couldn't connect to database.")

    cursor = db.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS main (
            guild_id TEXT,
            welc_text TEXT,
            msg_id_reaction TEXT,
            ch_id_welcome TEXT,
            ch_id_audit TEXT,
            ch_id_general TEXT,
            ch_id_admin TEXT
        );
    """
    )
    db.commit()
    print("Aju is ready.")


@bot.command(aliases=["csgo"])
async def aju_csgo(ctx, num: int):
    await ctx.send(web_scrape(num - 1))


@bot.command(
    aliases=[".", "..", "...", "....", ".....", "......", ".......", "........", ".........", "..........",]
)
async def ignore():
    try:
        pass
    except Exception:
        pass


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        responses = ["They aju ah niegey command ah.", "Aju ah egey ehthakaau keyfele."]
        await ctx.send(random.choice(responses))


@bot.event
async def on_cls_error(ctx, error):
    if isinstance(error, commands.MissingPermissions, commands.MissingAnyRole):
        responses = [
            "Adhi the command beynun vey varah ekalo bondo nivei.",
            "Hoho kanthethi.",
            "Nononono.",
            "U cannot la.",
        ]
        await ctx.send(random.choice(responses))


cogs = [
    "cogs.admin",
    "cogs.funny",
    "cogs.help",
    "cogs.image_downloader",
    "cogs.music",
    "cogs.roles",
    "cogs.set",
    "cogs.welcome",
]

if __name__ == "__main__":
    for cog in cogs:
        try:
            bot.load_extension(cog)
            print(f"{cog.replace('cogs.', '')} loaded succfully.")
        except Exception as cog_error:
            print(f"Couldn't load {cog.replace('cogs.', '')}\n")
            print(cog_error)

bot.run(os.environ["api_key"])
