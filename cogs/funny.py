import random
from typing import Union

import discord
from discord.ext import commands


class Funny(commands.Cog):
    """
    Beykaara commands
    """

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command()
    async def say(self, ctx: commands.Context, *, echo: str) -> None:
        sponged = []
        for char in echo:
            rand = random.randint(0, 1)
            if rand:
                sponged.append(char.upper())
            else:
                sponged.append(char.lower())
        sponged_text = "".join(sponged)
        await ctx.send(f"{sponged_text}")

    @commands.command()
    async def spam(self, ctx: commands.Context) -> None:
        spams = [
            "if Boombl4 has million number of fans i am one of them. if Boombl4 has ten fans i am one of them. if Boombl4 has no fans. that means i am no more on the earth. if world against Boombl4, i am against the world. i love Boombl4 till my last breath... die hard fan of Boombl4. Hit like if u think BoomBOoMbl4 best & smart in the world",
            "I'm Rick Harrison, and this is my pawn shop. I work here with my old man and my son, Big Hoss. Everything in here has a story and a price. One thing I've learned after 21 years - you never know what is gonna come through that door.",
            "So i was watching rick and morty right, and it was just a casual night and i was just watching rick and morty. Well, out of nowhere the funniest shit happened. Rick and Morty, Season 3, Episode 3, 56 seconds in. At the time, this was happening, The scientist guy, Rick, was nowhere to be found. Morty tried to look for him but all he found was just a mere little pickle on the desk. You know what happened? He heard ricks voice, somewhere around the room. Morty used a screwdriver to flip the pickle over and...you’ll never believe this, IT WAS RICK! HE WAS A PICKLE!! I kid you not, he’s called PICKLE RICK! PICKLE RICK!!! LMAO!!!! I was rolling on the floor laughing! My chest was in pain and i almost felt that i was going to suffocate!! Funniest shit i’d ever seen, i’ll tell you that. Im still laughing thinking about it. Awww man, you had to be there. It was just so funny.",
            "Simp means Sucker Idolizing Mediocre Pussy. A man is only a simp if the girl he is after has a mediocre pussy, but pokimane’s pussy is a goddess pussy, at worst. I will continue to donate 50% of my paycheck to pokimane because I know that it’s not simping. Poki if you see this I love you please text me back.",
            "Grow the fuck up. Leave furries alone and go back to your sad, pathetic, worthless lives masturbating to anime characters that will never love or care for you.",
            "What the fuck does “...” mean. Like what the fucking fuck you bitch. What the hell does three fucking dots mean. What are you trying to tell me that you can’t say with fucking words. What god damn message are you sending with those three fucking dots. Just use fucking words you fucking bitch. It’s not that fucking hard to speak fucking English you fucking stupid bitch. Fuck.",
            "What’s your favourite anime? Mines jojos bizarre adventure! Have you heard of that? Probably not. Its pretty unknown and unique. Its so good you should watch it. Have you watched it? You should totally watch it, its so good there are no animes like it. Im not like the other anime fans. I dont just watch mha and naruto, i watch the underground type shonen. Yeah, i know. Its pretty indie. So, anyway.. you should watch jojo its soooo amazing. Woah??! Your hat is the colour black?!??? IS THAT A JOJO REFERENCE. Yare yare daze. Btw im also a pedophile. And yes i know. Im not like the other guys either. Yeah, being a pedophile is pretty indie as well. Anyways, cya, i gotta go get my ribs removed so i can suck my own cock while watching jolyne hentai.",
            "I AM 19 AND LOCKED IN HOME FOR 3 FUCKING MONTHS. MY BEST YEARS ARE PROBABLY GONE. IT WILL PROBABLY TAKE YEARS FOR THE WORLD TO NORMALIZE. I WAS A FRESHMAN IN COLLEGE AND THEY WILL PROBABLY KEEP DOING THIS DISTANCE EDUCATION BULLSHIT. I AM YOUNG BUT WASTED. WHY? BECAUSE SOME CHINESE DOGSHIT FUCKING DISGUSTING FUCKING UGLY MAGGOT CUNT WANTED TO EAT SOME FUCKING BAT OR PANGOLIN OR WHATEVER THE FUCK THEY EAT FROM THOSE UTTERLY DISGUSTING, DIRTY AND FILTHY WET MARKETS. MY YOUTH IS FUCKING RUINED. IS THERE ANYTHING WORSE THAN THIS? IT IS LITERALLY FUCKING GONE. JUST GONE. WHEN WILL I BE ABLE TO FLIRT WITH A GIRL AGAIN? WHEN WILL I BE ABLE TO SOCIALIZE IN COLLEGE WITHOUT WORRYING ABOUT GETTING SICK AGAIN? WHEN WILL I BE ABLE TO HUG SOMEONE WITHOUT WORRYING AGAIN? WHEN WILL I BE ABLE TO SIT NEXT TO SOME FUCKING PERSON IN COLLEGE AGAIN? WHEN WILL I BE ABLE TO DATE SOMEONE AGAIN? FUCK THESE CHINGCHONG MOTHERFUCKERS",
            "Fuck you for having milk you piece of shit, and even more if you have sugar you fucking cunt bag fuck. Me drinking black coffee makes me essentially Jesus didn't you know. I'm fucking better than you. Fuck you for wanting something that tastes nice you fucking shit sock. Unless you're suffering every minute of drinking that coffee then you're doing it wrong and you should have been aborted. Fuck you you fucking cunt.",
            "Give it up folks, einstein over here has something to say. What's that buddy? Wha- A grammatical error?!? WHAT?!? B... Bu... That can't be possible! Surely not! A GRAMMAR MISTAKE? IN MY SIGHT?!? What a great, absolute miracle that you and your 257 IQ Brain was here to correct it! Thank you! Have my grattitude, Actually, What's your cashapp? I'd like to give you 20$... Know what? While we're at it have the keys to my car. Actually, no, scratch that. Have the keys to my house, go watch my kids grow up and fuck my wife. Also, my Paypal username and password is: Ilikesmartazzes4 and 968386329. Go have fun. Thank you for your work.",
            "Go ahead, call me lonely, a simp, or horny. These are MY FUCKING FEELINGS. I want to have the roughest and hottest sex with Belle Delphine. Seriously. Her cute accent, her lovely face, and her supple body drive me to horny madness. Every inch of her would be massaged and licked. When I want to finish and climax with all of my love, I would do it on her stomach, face, tits, and roll her over on her ass to blow the last of my load on those supple cheeks. I want to cuddle with her when I am done busting, and ask her how her day was, feeling each other's warmth on our naked, vulnerable bodies. She'd tell me how good it was and she'd confide her truest feelings to me, telling me how much she loves me. I would tell her I love her back, and she would give me a loving peck on my cheeks. Then we would get dressed and spend the day watching the Sopranos, still cuddling and even eating our favorite foods. I want Belle to be my girlfriend, my lover, my wife, and my life. I love her and want her to be mine. Is this a copy-pasta? No. I typed out every word to proclaim how I feel. Every time you ask who she is, look back on this: SHE IS MY WIFE. I love Belle Delphine, and these are MY original thoughts and feelings.",
            "I cannot FUCKING believe that Japanese-American musician Joji of 88rising is in actuality the popular Japanese-American YouTuber Joji Miller also know as Filthy Frank who was popular for his satirical content who has used a derogatory racial slur in his 2017 album ‘Pink Season’. I cannot believe this. I'm literally shaking. This can't be happening. My mom came into my room to bring me a plate of chicken nuggets and I literally screamed at her and hit the plate of chicken nuggets out of her hand. She started yelling and swearing at me and I slammed the door on her. I’m so distressed right now I don’t know what to do. I didn’t mean to do that to my mom but I’m literally in shock from the what happened today. I feel like I’m going to explode. This can’t be happening. I’m having a fucking breakdown. I don’t want to believe the world is so corrupt. I want a future to believe in. I cannot fucking deal with this right now. It wasn’t supposed to be like this. This is so fucked. I’m literally shaking right now... There’s no way Joji would do this... This can’t be real...",
            "To be fair, you have to have a very high IQ to understand Lil Pump. The humor is extremely subtle, and without a solid grasp of theoretical physics, most of the lyrics will go over a typical listener's head. There's also Lil Pump's nihilistic outlook, which is deftly woven into his characterization - his personal philosophy draws heavily from Narodnaya Volya, for instance. The fans understand this stuff; they have the intellectual capacity to truly appreciate the depths of these lyrics, to realize that they're not just catchy- they say something deep about LIFE. As a consequence people who dislike Lil Pump truly ARE idiots- of course they wouldn't appreciate, for instance, the humour in Lil Pump's existential catchphrase 'ESKITIT', which itself is a cryptic reference to Turgenev's Russian epic Fathers and Sons. I'm smirking right now just imagining one of those addlepated simpletons scratching their heads in confusion as Lil Pump's musical genius unfolds itself. What fools... how I pity them. And yes by the way, I DO have a Lil Pump tattoo. And no, you cannot see it. It's for the ladies' eyes only - And even they have to demonstrate that they're within five IQ points of my own (preferably lower) beforehand.",
            "Rawr X3 nuzzles How are you? pounces on you you're so warm o3o notices you have a bulge someone's happy! nuzzles your necky wecky ~murr~ hehe :wink: rubbies your bulgy wolgy you're so big! rubbies more on your bulgy wolgy it doesn't stop growing .///. kisses you and licks your neck daddy likes :wink: nuzzle wuzzle I hope daddy likes wiggles butt and squirms I wanna see your big daddy meat! wiggles butt I have a little itch o3o wags tails can you please get my itch? put paws on your chest nyea~ it's a seven inch itch rubs your chest can you pwease? squirms pwetty pwease? :frowning: I need to be punished runs paws down your chest and bites lip like, I need to be punished really good paws on your bulge as I lick my lips I'm getting thirsty. I could go for some milk unbuttons your pants as my eyes glow you smell so musky :wink: licks shaft mmmmmmmmmmmmmmmmmmm so musky :wink: drools all over your cawk your daddy meat. I like. Mister fuzzy balls. puts snout on balls and inhales deeply oh my gawd. I'm so hard rubbies your bulgy wolgy licks balls punish me daddy nyea~ squirms more and wiggles butt I9/11 lovewas an yourinside muskyjob goodness bites lip please punish me licks lips nyea~ suckles on your tip so good licks pre off your cock salty goodness~ eyes roll back and goes balls deep.",
            "Self control? Sex is sex, it's ingrained to HAVE sex. Wait until marriage? Some people never HAVE marriage. Just have sex? I think you should be able to see how that's failed. Just don't be a slut? Just don't have sex? Some people need sex. Assuming that's because I play nationstates? I've played that game for roughly less then a week, way less then I've believed in state sponsored prostitution. And I'm pretty sure they're adults with a need for sex. Anyways, I have to go, and for an actual fucking reason and not because I'm backing out of an argument, bring this up sometime else and I'll argue again.",
            "Bro, Lana Rhoades isn't hot. First off, she has a tattoo of someone named Jon on her ass so she's clearly already taken. Second, she's clearly unfaithful to him. Her gape isn't even that impressive either ive seen gapes that can fit a whole cucumber with like and extra finger or two. She just sucks bro like I could date her if I had money but she's bit even like a 10. With her troubled past and runins with the law id probably pass her up for like 6 or 7 with a good personality. You might think I have no room being picky, but I learned how to code during COVID and she wasn't careful with her firewalls I'd have her entire porn portfolio on a discord server with your name on it brew I gotchu. Yo but let's crush this crypto dude doge is cooling off a bit but cummies is about to moonnnn. Good catching up man sry bout tbe Lana Rhodes rant but can you blame me she's a fookin slag :joy:.",
        ]

        result = self.bot.config.find_one({"guild_id": ctx.guild.id, "ch_id_general": {"$exists": True}})

        if not result:
            await ctx.send(f"{random.choice(spams)}")
        else:
            if ctx.channel.id == result["ch_id_general"]:
                await ctx.send("Thebai nihigaahe mi channel aki.")
            else:
                await ctx.send(f"{random.choice(spams)}")

    @commands.command("avatar")
    async def avatar(self, ctx: commands.Context, *, member: Union[discord.Member, str, int]) -> None:
        if isinstance(member, discord.Member):
            embed = discord.Embed(
                title=f"{member}'s avatar",
                url=f"{member.avatar_url}",
                colour=discord.Colour(0xE9ACFD),
            )
            embed.set_image(url=member.avatar_url)
            await ctx.channel.purge(limit=1)
            await ctx.send(embed=embed)
        else:
            members = ctx.guild.members
            for m in members:
                if str(member).lower() in m.display_name.lower():
                    member = m
                    embed = discord.Embed(
                        title=f"{member}'s avatar",
                        url=f"{member.avatar_url}",
                        colour=discord.Colour(0xE9ACFD),
                    )
                    embed.set_image(url=member.avatar_url)
                    await ctx.channel.purge(limit=1)
                    await ctx.send(embed=embed)
                    break
            else:
                await ctx.send("Aju ah themeehaa nifenene.")

    @commands.command(aliases=["aju"])
    async def aju_bot(self, ctx: commands.Context) -> None:
        responses = [
            "I don't have an attitude I've got coronavirus and u can't handle it.",
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
            "I rike to uhh eat duh sticky rais.",
        ]
        await ctx.send(f"{random.choice(responses)}")

    # @aju_bot.error
    # async def on_aju_bot_error(self, ctx: commands.Context, error: commands.errors) -> None:
    #     if isinstance(error, commands.MissingRequiredArgument):
    #         responses = [
    #             "Wot?",
    #             "Eyn?",
    #             "O?",
    #             "Oo?",
    #             "Sup?",
    #             "Hm????",
    #             "P L E A S E  C O M P L E T E  T H E  S E N T E N C E .",
    #             "Aju kiyan koh dhey vee?",
    #         ]
    #         await ctx.send(random.choice(responses))


def setup(bot) -> None:
    bot.add_cog(Funny(bot))
