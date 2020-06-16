import youtube_dl
import discord
import shutil
import os
from discord.ext import commands

class Music(commands.Cog):

    queues = {}

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['j'])
    async def join(self, ctx):
        global voice
        channel = ctx.message.author.voice.channel
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)

        if voice and voice.is_connected():
            await voice.move_to(channel)

        else:
            voice = await channel.connect()

    @commands.command(aliases=['l'])
    async def leave(self, ctx):
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)

        if voice and voice.is_connected():
            await voice.disconnect()

    @commands.command(aliases=['p'])
    async def play(self, ctx, url:str):
        global voice
        channel = ctx.message.author.voice.channel
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)

        if voice and voice.is_connected():
            await voice.move_to(channel)

        else:
            voice = await channel.connect()

        def check_queue():
            queue_infile = os.path.isdir("./Queue")
            if queue_infile:
                q_dir = os.path.abspath(os.path.realpath("Queue"))
                length = len(os.listdir(q_dir))
                still_q = length - 1
                try:
                    file_1 = os.listdir(q_dir)[0]
                except:
                    print("Queue empty.")
                    self.queues.clear()
                    return
                main_path = os.path.dirname(os.path.realpath(__file__))
                song_path = os.path.dirname(f"{os.path.realpath('Queue')}/{file_1}")

                if length != 0:
                    print(f"Now playing: {still_q}")
                    song_there = os.path.isfile("song.mp3")
                    if song_there:
                        os.remove("song.mp3")
                    shutil.move(song_path, main_path)
                    for file in os.listdir("./"):
                        if file.endswith(".mp3"):
                            os.rename(file, "song.mp3")

                    voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: check_queue())
                    voice.source = discord.PCMVolumeTransformer(voice.source)
                    voice.source.volume = 0.07
                else:
                    self.queues.clear()
                    return

            else:
                    self.queues.clear()
                    print("No queued.")

        song_there = os.path.isfile("song.mp3")
        try:
            if song_there:
                os.remove("song.mp3")
                self.queues.clear()
                print("Removed old song file.")
        except PermissionError:
            print("Song is playing so cannot be deleted la.")
            await ctx.send("A song is already playing.")
            return
        
        queue_infile = os.path.isdir("./Queue")
        try:
            queue_folder = "./Queue"
            if queue_infile:
                print("Removed old queue folder.")
                shutil.rmtree(queue_folder)
        except:
            print("No old queue folder found.")

        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)

        ydl_args = {
            'format': 'bestaudio/best',
            'quiet': True,
            'postprocessors': [{
                'key': "FFmpegExtractAudio",
                'preferredcodec': "mp3",
                'preferredquality': "192",
            }],
        }

        with youtube_dl.YoutubeDL(ydl_args) as ydl:
            print("Downloading audio.")
            ydl.download([url])

        for file in os.listdir("./"):
            if file.endswith(".mp3"):
                name = file
                print(f"Renamed {file}")
                os.rename(file, "song.mp3")

        voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: check_queue())
        voice.source = discord.PCMVolumeTransformer(voice.source)
        voice.source.volume = 0.07

        name_split = name.rsplit("-", 2)
        await ctx.send(f"Playing: {name_split[0]}")
        print(f"Playing song {name_split}")

    @commands.command(aliases=['pa'])
    async def pause(self, ctx):
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)

        if voice and voice.is_playing():
            voice.pause()
            print("Paused music.")
            await ctx.send("Paused music.")
        else:
            print("Failed pause no music playing.")
            await ctx.send("Nothing playing.")

    @commands.command(aliases=['r'])
    async def resume(self, ctx):
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)

        if voice and voice.is_paused():
            voice.resume()
            print("Resumed music.")
            await ctx.send("Paused music.")
        else:
            print("Music not paused.")
            await ctx.send("Music not paused.")

    @commands.command(aliases=['s'])
    async def skip(self, ctx):
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)

        self.queues.clear()

        if voice and voice.is_playing():
            voice.stop()
            print("Skipped track.")
            await ctx.send("Skipped current track.")
        else:
            print("No music playing.")
            await ctx.send("No music playing.")
    
    @commands.command(aliases=['q'])
    async def queue(self, ctx, url:str):
        queue_infile = os.path.isdir("./Queue")
        if not queue_infile:
            os.mkdir("Queue")
        q_dir = os.path.abspath(os.path.realpath("Queue"))
        q_num = len(os.listdir(q_dir))
        q_num += 1
        add_queue = True        
        while add_queue:
            if q_num in self.queues:
                q_num += 1
            else:
                add_queue = False
                self.queues[q_num] = q_num

        q_path = os.path.dirname(f"{os.path.realpath('Queue')}/song{q_num}.%(ext)s")

        ydl_args = {
            'format': 'bestaudio/best',
            'quiet': True,
            'outtmpl': q_path,
            'postprocessors': [{
                'key': "FFmpegExtractAudio",
                'preferredcodec': "mp3",
                'preferredquality': "192",
            }],
        }

        with youtube_dl.YoutubeDL(ydl_args) as ydl:
            print("Downloading audio.")
            ydl.download([url])
        
        await ctx.send(f"Added {q_num} to the queue.")
        print("Song added to queue.")


def setup(bot):
    bot.add_cog(Music(bot))