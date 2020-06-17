import youtube_dl
import discord
import shutil
import os
import asyncio
from discord.ext import commands

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


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
            await ctx.send(f"Joined {channel}")

    @commands.command(aliases=['dc'])
    async def leave(self, ctx):
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)

        if voice and voice.is_connected():
            await voice.disconnect()

    @commands.command(aliases=['p'])
    async def play(self, ctx, *, url:str):
        global voice
        channel = ctx.message.author.voice.channel
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)

        if voice and voice.is_connected():
            await voice.move_to(channel)

        else:
            voice = await channel.connect()

        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
            ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

        embed = discord.Embed(
            colour=discord.Colour(0xe9acfd)
        )
        embed.add_field(name=f"Now playing:", value=f"[{player.title}]({url})")
        embed.set_footer(text=f"Requested by: {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(aliases=['ps'])
    async def pause(self, ctx):
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)

        if voice and voice.is_playing():
            voice.pause()
            print("Paused ⏸.")
            await ctx.send("Paused music.")
        else:
            print("Failed pause no music playing.")
            await ctx.send("Nothing playing.")

    @commands.command(aliases=['r'])
    async def resume(self, ctx):
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)

        if voice and voice.is_paused():
            voice.resume()
            print("Resumed ▶.")
            await ctx.send("Resumed music.")
        else:
            print("Music not paused.")
            await ctx.send("Nothing paused.")

    @commands.command(aliases=['s'])
    async def skip(self, ctx):
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)

        # self.queues.clear()

        if voice and voice.is_playing():
            voice.stop()
            print("Skipped track.")
            await ctx.send("Skipped current track.")
        else:
            print("No music playing.")
            await ctx.send("Nothing playing.")

    @commands.command()
    async def volume(self, ctx, volume: int):
        if ctx.voice_client is None:
            return await ctx.send("Not connected to a voice channel.")

        ctx.voice_client.source.volume = volume / 100
        await ctx.send(f"Changed volume to {volume}%")

    # @commands.command(aliases=['q'])
    # async def queue(self, ctx, url:str):



def setup(bot):
    bot.add_cog(Music(bot))