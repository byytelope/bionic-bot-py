import youtube_dl
import discord
import shutil
import os
import asyncio
import urllib.parse, urllib.request, re
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

    @staticmethod
    def from_query(query):
        query_string = urllib.parse.urlencode({
            'search_query': query
        })
        htm_content = urllib.request.urlopen(
            f"https://www.youtube.com/results?{query_string}"
        )
        search_results = re.findall('href=\"\\/watch\\?v=(.{11})', htm_content.read().decode())
        return f"https://www.youtube.com/watch?v={search_results[0]}"

class Music(commands.Cog):

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
    async def stop(self, ctx):
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

        embed = discord.Embed(
            colour=discord.Colour(0xe9acfd)
        )
        embed.set_footer(text=f"Requested by: {ctx.author}", icon_url=ctx.author.avatar_url)

        if url.startswith("https:") or url.startswith("www."):
            async with ctx.typing():
                player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
                ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
                embed.add_field(name=f"Now playing:", value=f"[{player.title}]({url})")
        else:
            async with ctx.typing():
                url_parsed = YTDLSource.from_query(url)
                player = await YTDLSource.from_url(url_parsed, loop=self.bot.loop, stream=True)
                ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
                embed.add_field(name=f"Now playing:", value=f"[{player.title}]({url_parsed})")

        await ctx.send(embed=embed, delete_after=15)

    @commands.command(aliases=['ps'])
    async def pause(self, ctx):
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)

        if voice and voice.is_playing():
            voice.pause()
            print("Paused music.")
            await ctx.send("Paused ⏸")
        else:
            print("Failed pause no music playing.")
            await ctx.send("Nothing playing.")

    @commands.command(aliases=['r'])
    async def resume(self, ctx):
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)

        if voice and voice.is_paused():
            voice.resume()
            print("Resumed music.")
            await ctx.send("Resumed ▶")
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

    @commands.command(aliases=['v', 'vol'])
    async def volume(self, ctx, volume: int):
        if ctx.voice_client is None:
            return await ctx.send("Not connected to a voice channel.")

        ctx.voice_client.source.volume = volume / 100
        await ctx.send(f"Changed volume to {volume}%")

    # @commands.command(aliases=['q'])
    # async def queue(self, ctx, url:str):

    @play.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError("Author not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()


def setup(bot):
    bot.add_cog(Music(bot))