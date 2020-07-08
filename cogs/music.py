import asyncio
import discord
import itertools
import json
import math
import random
import youtube_dl

from async_timeout import timeout
from discord.ext import commands
from validator_collection import checkers
from youtubesearchpython import searchYoutube

YTDL_OPTIONS = {
    "format": "bestaudio/best",
    "outtmpl": "%(extractor)s-%(id)s-%(title)s.%(ext)s",
    "restrictfilenames": True,
    "noplaylist": True,
    "nocheckcertificate": True,
    "ignoreerrors": False,
    "logtostderr": False,
    "quiet": True,
    "no_warnings": True,
    "default_search": "auto",
    "source_address": "0.0.0.0",
}

FFMPEG_OPTIONS = {"options": "-vn -reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 4"}

ytdl = youtube_dl.YoutubeDL(YTDL_OPTIONS)


class VoiceError(Exception):
    pass


class YTDLError(Exception):
    pass


class YTDLSource(discord.PCMVolumeTransformer):
    """
    Source for ytdl
    """

    def __init__(self, source: discord.FFmpegPCMAudio, *, data: dict, volume: float = 1.0):
        super().__init__(source, volume)

        self.data = data
        self.title = data.get("title")
        self.thumbnail = data.get("thumbnail")
        self.duration = self.parse_duration(int(data.get("duration")))
        self.url = data.get("url")

    def __str__(self):
        return f"**{self.title}** by **{self.uploader}**"

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if "entries" in data:
            data = data["entries"][0]

        filename = data["url"] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **FFMPEG_OPTIONS), data=data)

    @staticmethod
    def from_query(query):
        yt_response = searchYoutube(query, offset=1, mode="json", max_results=1)
        result = json.loads(yt_response.result())
        yt_link = result["search_result"][0]["link"]
        return yt_link

    @staticmethod
    def parse_duration(duration: int):
        minutes, seconds = divmod(duration, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)

        duration = []
        if days > 0:
            duration.append(f"{days} days")
        if hours > 0:
            duration.append(f"{hours} hours")
        if minutes > 0:
            duration.append(f"{minutes} minutes")
        if seconds > 0:
            duration.append(f"{seconds} seconds")

        return ", ".join(duration)


class SongQueue(asyncio.Queue):
    def __getitem__(self, item):
        if isinstance(item, slice):
            return list(itertools.islice(self._queue, item.start, item.stop, item.step))
        else:
            return self._queue[item]

    def __iter__(self):
        return self._queue.__iter__()

    def __len__(self):
        return self.qsize()

    def clear(self):
        self._queue.clear()

    def shuffle(self):
        random.shuffle(self._queue)

    def remove(self, index: int):
        del self._queue[index]


class VoiceState:
    def __init__(self, bot: commands.Bot, ctx: commands.Context):
        self.bot = bot
        self._ctx = ctx

        self.current = None
        self.voice = None
        self.next = asyncio.Event()
        self.songs = SongQueue()

        self._loop = False
        self._volume = 1.0
        self.skip_votes = set()

        self.audio_player = bot.loop.create_task(self.audio_player_task())

    def __del__(self):
        self.audio_player.cancel()

    @property
    def loop(self):
        return self._loop

    @loop.setter
    def loop(self, value: bool):
        self._loop = value

    @property
    def volume(self):
        return self._volume

    @volume.setter
    def volume(self, value: float):
        self._volume = value

    @property
    def is_playing(self):
        return self.voice and self.current

    async def audio_player_task(self):
        while True:
            self.next.clear()

            if not self.loop:
                # Try to get the next song within 3 minutes.
                # If no song will be added to the queue in time,
                # the player will disconnect due to performance
                # reasons.
                try:
                    async with timeout(180):  # 3 minutes
                        self.current = await self.songs.get()
                except asyncio.TimeoutError:
                    self.bot.loop.create_task(self.stop())
                    return

            self.current.source.volume = self._volume
            self.voice.play(self.current.source, after=self.play_next_song)
            await self.current.source.channel.send(embed=self.current.create_embed())

            await self.next.wait()

    def play_next_song(self, error=None):
        if error:
            raise VoiceError(str(error))

        self.next.set()

    def skip(self):
        self.skip_votes.clear()

        if self.is_playing:
            self.voice.stop()

    async def stop(self):
        self.songs.clear()

        if self.voice:
            await self.voice.disconnect()
            self.voice = None


class Music(commands.Cog):
    """
    Main music class
    """

    def __init__(self, bot):
        self.bot = bot
        self.voice_states = {}

    def get_voice_state(self, ctx: commands.Context):
        state = self.voice_states.get(ctx.guild.id)
        if not state:
            state = VoiceState(self.bot, ctx)
            self.voice_states[ctx.guild.id] = state

        return state

    def cog_unload(self):
        for state in self.voice_states.values():
            self.bot.loop.create_task(state.stop())

    def cog_check(self, ctx: commands.Context):
        if not ctx.guild:
            raise commands.NoPrivateMessage("This command can't be used in DM channels.")

        return True

    @commands.command(aliases=["j"])
    async def join(self, ctx, *, channel: discord.VoiceChannel = None):
        channel = ctx.message.author.voice.channel

        if ctx.voice_state.voice:
            await ctx.voice_state.voice.move_to(channel)
            return

        ctx.voice_state.voice = await channel.connect()

    @commands.command(aliases=["dc"])
    async def stop(self, ctx):
        if not ctx.voice_state.voice:
            return await ctx.send("Not connected to any voice channel.")

        await ctx.voice_state.stop()
        await ctx.message.add_reaction("⏹")
        del self.voice_states[ctx.guild.id]

    @commands.command(aliases=["p"])
    async def play(self, ctx, *, url: str):
        if not ctx.voice_state.voice:
            await ctx.invoke(self.join)

        embed = discord.Embed(colour=discord.Colour(0xE9ACFD)).set_footer(
            text=f"Requested by: {ctx.author}", icon_url=ctx.author.avatar_url
        )

        try:
            if checkers.is_url(url):
                async with ctx.typing():
                    player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
                    ctx.voice_client.play(player, after=lambda e: print("Player error: %s" % e) if e else None)
                    embed.add_field(name="Now playing:", value=f"[{player.title}]({url})", inline=False)
                    embed.add_field(name="Duration", value=player.duration, inline=False)
                    embed.set_thumbnail(url=player.thumbnail)
            else:
                async with ctx.typing():
                    url_parsed = YTDLSource.from_query(url)
                    player = await YTDLSource.from_url(url_parsed, loop=self.bot.loop, stream=True)
                    ctx.voice_client.play(player, after=lambda e: print("Player error: %s" % e) if e else None)
                    embed.add_field(name="Now playing:", value=f"[{player.title}]({url_parsed})", inline=False)
                    embed.add_field(name="Duration", value=player.duration, inline=False)
                    embed.set_thumbnail(url=player.thumbnail)
            await ctx.send(embed=embed)
        except YTDLError as e:
            await ctx.send(f"An error occurred while processing this request: {str(e)}")
        else:
            await ctx.voice_state.songs.put()
            await ctx.send(f"Queued {str(player)}")

    @commands.command(aliases=["ps"])
    async def pause(self, ctx):
        if not ctx.voice_state.is_playing and ctx.voice_state.voice.is_playing():
            ctx.voice_state.voice.pause()
            await ctx.message.add_reaction("⏸")

    @commands.command(aliases=["r"])
    async def resume(self, ctx):
        if not ctx.voice_state.is_playing and ctx.voice_state.voice.is_paused():
            ctx.voice_state.voice.resume()
            await ctx.message.add_reaction("▶")

    @commands.command(aliases=["s"])
    async def skip(self, ctx):
        if not ctx.voice_state.is_playing:
            return await ctx.send("Not playing any music right now...")

        await ctx.message.add_reaction("⏭")
        ctx.voice_state.skip()

    @commands.command(aliases=["v", "vol"])
    async def volume(self, ctx, volume: int):
        if not ctx.voice_state.is_playing:
            return await ctx.send("Nothing being played at the moment.")

        if 0 > volume > 100:
            return await ctx.send("Volume must be between 0 and 100")

        ctx.voice_state.volume = volume / 100
        await ctx.send(f"Volume of the player set to {volume}%")

    @commands.command(aliases=["l"])
    async def loop(self, ctx):
        if not ctx.voice_state.is_playing:
            return await ctx.send("Nothing being played at the moment.")

        ctx.voice_state.loop = not ctx.voice_state.loop
        await ctx.message.add_reaction("🔂")

    @commands.command(aliases=["shuf"])
    async def shuffle(self, ctx):
        if len(ctx.voice_state.songs) == 0:
            return await ctx.send("Empty queue.")

        ctx.voice_state.songs.shuffle()
        await ctx.message.add_reaction("🔀")

    @commands.command(aliases=["q"])
    async def queue(self, ctx, page: int = 1):
        if len(ctx.voice_state.songs) == 0:
            return await ctx.send("Empty queue.")

        items_per_page = 10
        pages = math.ceil(len(ctx.voice_state.songs) / items_per_page)

        start = (page - 1) * items_per_page
        end = start + items_per_page

        queue = ""
        for i, song in enumerate(ctx.voice_state.songs[start:end], start=start):
            queue += "`{0}.` [**{1.source.title}**]({1.source.url})\n".format(i + 1, song)

        embed = discord.Embed(description=f"**{len(ctx.voice_state.songs)} tracks:**\n\n{queue}").set_footer(
            text=f"Viewing page {page}/{pages}"
        )
        await ctx.send(embed=embed)

    @commands.command(aliases=["current", "playing", "now_playing"])
    async def now(self, ctx):
        await ctx.send(embed=ctx.voice_state.current.create_embed())

    @commands.command(aliases=["rem"])
    async def remove(self, ctx, index: int):
        if len(ctx.voice_state.songs) == 0:
            return await ctx.send("Empty queue.")

        ctx.voice_state.songs.remove(index - 1)
        await ctx.message.add_reaction("✅")

    # @commands.command(aliases=['q'])
    # async def queue(self, ctx, url:str):

    @join.before_invoke
    @play.before_invoke
    async def ensure_voice_state(self, ctx):
        ctx.voice_state = self.get_voice_state(ctx)

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
