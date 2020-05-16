import random
import discord
import COVID19Py
import os
from discord.ext import commands
from web_scraper import web_scrape

covid19 = COVID19Py.COVID19("https://coronavirus-tracker-api.herokuapp.com").getLatest()

bot = commands.Bot(command_prefix=".")
bot.remove_command('help')

id_bionic = 585576337041784862


@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("use .help for help"))
    print("Bot be ready.")


@bot.command()
async def help(ctx):

    embed=discord.Embed(
        colour=discord.Colour.blurple(),
        title='Use a "." before command',
        description='How 2 use Aju'
    )
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/592639239683047424/711173474592489543/unknown.png")
    embed.add_field(name='aju', value="Talk to Aju when you're bored.", inline=False)
    embed.add_field(name='corona', value="Use corona confirmed for confirmed and corona deaths for deaths.", inline=False)
    embed.add_field(name='members', value='Aju will count the number of members in the server.', inline=False)
    embed.add_field(name='spam', value="Don't.", inline=False)
    embed.add_field(name='csgo', value='HLTV rankings for all time best CS:GO players.', inline=False)
    embed.add_field(name='cls (Admin role required)', value='Aju will erase a defined number of messages for you. Default value is 3.', inline=False)
    embed.set_footer(text='Be nice to Aju thank.')

    await ctx.send(embed=embed)

@bot.command()
@commands.has_any_role('Chernobyl', 'Three Mile Island', 'Covid-19')
@commands.has_permissions(manage_messages=True)
async def cls(ctx, amount=3):
    await ctx.channel.purge(limit=amount)


@bot.command(aliases=["members"])
async def aju_members(ctx, *, members):
    server_id = bot.get_guild(id_bionic)
    await ctx.send(f"There are {server_id.member_count} corona-free people in bionic.")


@bot.command(aliases=["ping"])
async def aju_ping(ctx):
    await ctx.send(f"{round(bot.latency * 1000)}ms in thiyaa aju ah libenei.")


@bot.command(aliases=["spam"])
async def aju_spam(ctx):
    await ctx.send("So i was watching rick and morty right, and it was just a casual night and i was just watching rick and morty. Well, out of nowhere the funniest shit happened. Rick and Morty, Season 3, Episode 3, 56 seconds in. At the time, this was happening, The scientist guy, Rick, was nowhere to be found. Morty tried to look for him but all he found was just a mere little pickle on the desk. You know what happened? He heard ricks voice, somewhere around the room. Morty used a screwdriver to flip the pickle over and...you’ll never believe this, IT WAS RICK! HE WAS A PICKLE!! I kid you not, he’s called PICKLE RICK! PICKLE RICK!!! LMAO!!!! I was rolling on the floor laughing! My chest was in pain and i almost felt that i was going to suffocate!! Funniest shit i’d ever seen, i’ll tell you that. Im still laughing thinking about it. Awww man, you had to be there. It was just so funny.")


@bot.command(aliases=["csgo"])
async def aju_csgo(ctx, num: int):
    await ctx.send(web_scrape(num-1))


@bot.command(aliases=["aju"])
async def aju_bot(ctx, *, hello):
    responses = ["I don't have an attitude I've got coronavirus and u can't handle it.",
                 "I'm fine.",
                 "I'm vegan.",
                 "I'm on a seafood diet. I see food and I eat it.",
                 "If you are not coffee, chocolate, or coronavirus, I'm gonna need u to go away.",
                 "I hate running. You know what I love though? Coronavirus.",
                 "That's it! I'm calling China.",
                 "They aju dhenne meehakee?",
                 "Achoo. U are now corona-aladeen.",
                 "Heil Kim Jong-Un.",
                 "Hanagen aase.",
                 "I rike to uhh eat duh sticky rais."]
    await ctx.send(f"{random.choice(responses)}")


@bot.command(aliases=["corona"])
async def aju_number(ctx, value: str):
    await ctx.send(f"{covid19[value]} hei meehun.")


@cls.error
async def on_cls_error(ctx, error):
    if isinstance(error, commands.MissingPermissions) or isinstance(error, commands.MissingAnyRole):
        await ctx.send("Adhi the command beynun vey varah ekalo bondo nivei.")


@aju_bot.error
async def on_aju_bot_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        responses = ["Wot?",
                     "Eyn?",
                     "O?",
                     "Oo?",
                     "Sup?",
                     "Hm????",
                     "P L E A S E  C O M P L E T E  T H E  S E N T E N C E .",
                     "Aju kiyan koh dhey vee?"]
        await ctx.send(random.choice(responses))


@aju_number.error
async def on_aju_number_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        responses = ["Corona cowcow?",
                     "Adhi ada neevene ey.",
                     "Thankeda baaraa benafele.",
                     "Corona wot?",
                     "Thehen ekani benagen keraah vee kamah aju ah egei?"]
        await ctx.send(random.choice(responses))


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        responses = ["They aju ah niegey command ah.",
                     "Aju ah egey ehthakaau keyfele."]
        await ctx.send(random.choice(responses))


bot.run(os.environ['api_key'])
