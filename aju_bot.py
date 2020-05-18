import discord
import random
import os
from discord.ext import commands

bot = commands.Bot(command_prefix=".")
bot.remove_command('help')

@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("use .help for help"))
    print("Bot be ready.")


@bot.command(aliases=["ping"])
async def aju_ping(ctx):
    await ctx.send(f"{round(bot.latency * 1000)}ms in thiyaa aju ah libenei.")


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        responses = ["They aju ah niegey command ah.",
                     "Aju ah egey ehthakaau keyfele."]
        await ctx.send(random.choice(responses))

bot.load_extension('cogs.HelpCommands')
bot.load_extension('cogs.ReactionRoles')
bot.load_extension('cogs.Funny')
bot.load_extension('cogs.AdminCommands')

bot.run(os.environ['api_key'])
