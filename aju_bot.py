import discord
import random
import os
import psycopg2
from web_scraper import web_scrape
from discord.ext import commands

bot = commands.Bot(command_prefix=".")
bot.remove_command('help')


@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("use .help for help"))
    print("Bot be ready.")
    
    DATABASE_URL = os.getenv("DATABASE_URL")
    db = psycopg2.connect(DATABASE_URL, sslmode="require")
    cursor = db.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS main(
        guild_id TEXT PRIMARY KEY,
        welc_text TEXT,
        msg_id_reaction TEXT,
        ch_id_welcome TEXT,
        ch_id_audit TEXT,
        ch_id_general TEXT,
        ch_id_admin TEXT
    );
    ''')
    db.commit()
    print("Heroku pg ready.")

@bot.command(aliases=["csgo"])
async def aju_csgo(self, ctx, num: int):
    await ctx.send(web_scrape(num-1))

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        responses = ["They aju ah niegey command ah.",
                    "Aju ah egey ehthakaau keyfele."]
        await ctx.send(random.choice(responses))


bot.load_extension('cogs.HelpCommands')
bot.load_extension('cogs.Roles')
bot.load_extension('cogs.Funny')
bot.load_extension('cogs.AdminCommands')
bot.load_extension('cogs.Welcome')
bot.load_extension('cogs.Set')

bot.run(os.environ['api_key'])