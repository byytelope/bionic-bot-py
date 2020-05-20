import discord
import random
import os
from web_scraper import web_scrape
from discord.ext import commands

bot = commands.Bot(command_prefix=".")
bot.remove_command('help')


@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("use .help for help"))
    print("Bot be ready.")

@bot.command(aliases=["csgo"])
async def aju_csgo(self, ctx, num: int):
    await ctx.send(web_scrape(num-1))

@bot.event
async def on_raw_reaction_add(payload):
    message_id = payload.message_id
    if message_id == 711977846112911490:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda f: f.id == guild_id, bot.guilds)

        role = discord.utils.get(guild.roles, name=payload.emoji.name)

        if role is not None:
            member = discord.utils.find(lambda ree: ree.id == payload.user_id, guild.members)
            if member is not None:
                await member.add_roles(role)
                print(f"Added {role} to {member}")
            else:
                print("Member not found.")
        else:
            print("Role not found.")

@bot.event
async def on_raw_reaction_remove(payload):
    message_id = payload.message_id
    if message_id == 711977846112911490:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda bruh: bruh.id == guild_id, bot.guilds)

        role = discord.utils.get(guild.roles, name=payload.emoji.name)

        if role is not None:
            member = discord.utils.find(lambda ree: ree.id == payload.user_id, guild.members)
            if member is not None:
                await member.remove_roles(role)
                print(f"Removed {role} from {member}")
            else:
                print("Member not found.")
        else:
            print("Role not found.")

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

bot.run(os.environ['api_key'])