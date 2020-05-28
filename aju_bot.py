import discord
import psycopg2
import random
import os
from web_scraper import web_scrape
from discord.ext import commands

bot = commands.Bot(command_prefix=".", owner_id=367686193242177536)
bot.remove_command('help')


@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("use .help for help"))

    db_database = os.environ['db_database']
    db_user = os.environ['db_user']
    db_password = os.environ['db_password']
    db_host = os.environ['db_host']
    db_port = os.environ['db_port']

    try:
        db = psycopg2.connect(
            database=db_database,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port
            )
        print('db con succ')
    except psycopg2.OperationalError as e:
        print(e)
        print('db con not succ')

    cursor = db.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS main (
            guild_id TEXT,
            welc_text TEXT,
            msg_id_reaction TEXT,
            ch_id_welcome TEXT,
            ch_id_audit TEXT,
            ch_id_general TEXT,
            ch_id_admin TEXT
        );
    ''')
    db.commit()
    print("Bot be ready.")

@bot.command(aliases=["csgo"])
async def aju_csgo(ctx, num: int):
    await ctx.send(web_scrape(num-1))

@bot.command(aliases=['.','..','...','....','.....','......','.......'])
async def ignore(ctx):
    pass

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        responses = ["They aju ah niegey command ah.",
                    "Aju ah egey ehthakaau keyfele."]
        await ctx.send(random.choice(responses))

@bot.event
async def on_cls_error(ctx, error):
    if isinstance(error, commands.MissingPermissions) or isinstance(error, commands.MissingAnyRole):
        responses = [
            'Adhi the command beynun vey varah ekalo bondo nivei.',
            'Hoho kanthethi.',
            'Nononono.',
            'U cannot la.'
                ]
        await ctx.send(random.choice(responses))


bot.load_extension('cogs.HelpCommands')
bot.load_extension('cogs.Roles')
bot.load_extension('cogs.Funny')
bot.load_extension('cogs.AdminCommands')
bot.load_extension('cogs.Welcome')
bot.load_extension('cogs.Set')

bot.run(os.environ['api_key'])