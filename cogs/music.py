import asyncio
import functools
import itertools
import math
import random

import discord
import youtube_dl
from async_timeout import timeout
from discord.channel import VoiceChannel
from discord.ext import commands

# youtube_dl.utils.bug_reports_message = lambda: ""


class VoiceError(Exception):
    pass


class YTDLError(Exception):
    pass


class YTDLSource(discord.PCMVolumeTransformer):
    """
    Source for ytdl
    """

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
        "source_address": "0.0.0.0"
        # "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.85 Safari/537.36",
    }

    FFMPEG_OPTIONS = {"options": "-vn -reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"}

    ytdl = youtube_dl.YoutubeDL(YTDL_OPTIONS)

    def __init__(self, ctx: commands.Context, source: discord.FFmpegPCMAudio, *, data: dict, volume: float = 1.0):
        super().__init__(source, volume)
        self.requester = ctx.author
        self.channel = ctx.channel
        self.data = data
        self.song_progress = 0
        self.title = data.get("title")
        self.thumbnail = data.get("thumbnail")
        self.duration = self.parse_duration(int(data.get("duration")))
        self.url = data.get("url")

    def __str__(self):
        return f"**{self.title}**"

    @classmethod
    async def create_source(cls, ctx: commands.Context, search: str, *, loop: asyncio.BaseEventLoop = None):
        loop = loop or asyncio.get_event_loop()

        partial = functools.partial(cls.ytdl.extract_info, search, download=False, process=False)
        data = await loop.run_in_executor(None, partial)

        if data is None:
            raise YTDLError(f"Couldn't find anything that matches `{search}`")

        if "entries" not in data:
            process_info = data
        else:
            process_info = None
            for entry in data["entries"]:
                if entry:
                    process_info = entry
                    break

            if process_info is None:
                raise YTDLError(f"Couldn't find anything that matches `{search}`")

        webpage_url = process_info["webpage_url"]
        partial = functools.partial(cls.ytdl.extract_info, webpage_url, download=False)
        processed_info = await loop.run_in_executor(None, partial)

        if processed_info is None:
            raise YTDLError(f"Couldn't fetch `{webpage_url}`")

        if "entries" not in processed_info:
            info = processed_info
        else:
            info = None
            while info is None:
                try:
                    info = processed_info["entries"].pop(0)
                except IndexError:
                    raise YTDLError(f"Couldn't retrieve any matches for `{webpage_url}`")

        return cls(ctx, discord.FFmpegPCMAudio(info["url"], **cls.FFMPEG_OPTIONS), data=info)

    @staticmethod
    def parse_duration(duration: int):
        minutes, seconds = divmod(duration, 60)
        if seconds < 10:
            seconds = f"{seconds:02d}"
        duration = []
        duration.append(str(minutes))
        duration.append(str(seconds))

        return ":".join(duration)


class Song:
    __slots__ = ("source", "requester")

    def __init__(self, source: YTDLSource):
        self.source = source
        self.requester = source.requester

    def create_embed(self):
        embed = (
            discord.Embed(color=discord.Colour(0xE9ACFD))
            .add_field(
                name="Now playing:",
                value=f"**[{self.source.title}]({self.source.url})**\nDuration: ***{self.source.duration}***",
                inline=False,
            )
            .set_thumbnail(url=self.source.thumbnail)
            .set_footer(text=f"Requested by: {self.requester}", icon_url=self.requester.avatar_url)
        )

        return embed


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

    # @property
    # def progress(self):
    #     if self.source:
    #         return self.source.song_progress
    #     else:
    #         raise VoiceError("No song playing...")
    #         return 0

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
            await self.current.source.channel.send(embed=self.current.create_embed(), delete_after=60)

            await self.next.wait()

    def play_next_song(self, error=None):
        if error:
            raise VoiceError(str(error))

        self.next.set()

    def skip(self):
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

    def __init__(self, bot: commands.Bot):
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

    async def cog_before_invoke(self, ctx: commands.Context):
        ctx.voice_state = self.get_voice_state(ctx)

    async def cog_command_error(self, ctx: commands.Context, error: commands.CommandError):
        await ctx.send(f"An error occurred: {str(error)}")

    @commands.command(name="join", aliases=["j"], invoke_without_subcommand=True)
    async def _join(self, ctx: commands.Context, *, channel: discord.VoiceChannel = None):
        channel = ctx.message.author.voice.channel

        if ctx.voice_state.voice:
            await ctx.voice_state.voice.move_to(channel)
            return

        ctx.voice_state.voice = await channel.connect()

    @commands.command(name="stop", aliases=["dc", "disconnect", "leave"])
    async def _stop(self, ctx: commands.Context):
        if not ctx.voice_state.voice:
            return await ctx.send("Not connected to any voice channel.")

        await ctx.voice_state.stop()
        await ctx.message.add_reaction("⏹")
        del self.voice_states[ctx.guild.id]

    @commands.command(name="play", aliases=["p"])
    async def _play(self, ctx: commands.Context, *, search: str):
        if not ctx.voice_state.voice:
            await ctx.invoke(self._join)

        async with ctx.typing():
            try:
                source = await YTDLSource.create_source(ctx, search, loop=self.bot.loop)
            except YTDLError as e:
                await ctx.send(f"An error occurred while processing this request: {str(e)}")
            else:
                if len(ctx.voice_state.songs) >= 1 or ctx.voice_client.is_playing():
                    embed = discord.Embed(
                        title="Queued:",
                        description=f"[{source.title}]({source.url})",
                        colour=discord.Colour(0xE9ACFD),
                    )
                    await ctx.send(embed=embed)

                song = Song(source)
                await ctx.voice_state.songs.put(song)

    @commands.command(name="pause", aliases=["ps"])
    async def _pause(self, ctx: commands.Context):
        if not ctx.voice_state.is_playing and ctx.voice_state.voice.is_playing():
            ctx.voice_state.voice.pause()
            await ctx.message.add_reaction("⏸")

    @commands.command(name="resume", aliases=["r"])
    async def _resume(self, ctx: commands.Context):
        if not ctx.voice_state.is_playing and ctx.voice_state.voice.is_paused():
            ctx.voice_state.voice.resume()
            await ctx.message.add_reaction("▶")

    @commands.command(name="skip", aliases=["s"])
    async def _skip(self, ctx: commands.Context):
        if not ctx.voice_state.is_playing:
            return await ctx.send("Not playing any music right now...")

        await ctx.message.add_reaction("⏭")
        ctx.voice_state.skip()

    @commands.command(name="volume", aliases=["v", "vol"])
    async def _volume(self, ctx: commands.Context, volume: int):
        if not ctx.voice_state.is_playing:
            return await ctx.send("Nothing being played at the moment.")
        elif volume / 100 == ctx.voice_state.current.source.volume:
            return await ctx.send(f"Volume is already at {volume}%")
        elif 0 > volume > 100:
            return await ctx.send("Volume must be between 0 and 100")
        else:
            ctx.voice_state.current.source.volume = volume / 100
            await ctx.send(f"Volume set to {volume}%")

    @commands.command(name="loop", aliases=["l"])
    async def _loop(self, ctx: commands.Context):
        if not ctx.voice_state.is_playing:
            return await ctx.send("Nothing being played at the moment.")

        ctx.voice_state.loop = not ctx.voice_state.loop
        await ctx.message.add_reaction("🔂")

    @commands.command(name="shuffle", aliases=["shuf"])
    async def _shuffle(self, ctx: commands.Context):
        if len(ctx.voice_state.songs) == 0:
            return await ctx.send("No songs in queue.")

        ctx.voice_state.songs.shuffle()
        await ctx.message.add_reaction("🔀")

    @commands.command(name="queue", aliases=["q"])
    async def _queue(self, ctx: commands.Context, page: int = 1):
        if len(ctx.voice_state.songs) == 0:
            return await ctx.send("No songs in queue.")

        items_per_page = 10
        pages = math.ceil(len(ctx.voice_state.songs) / items_per_page)

        start = (page - 1) * items_per_page
        end = start + items_per_page

        queue = ""
        for i, song in enumerate(ctx.voice_state.songs[start:end], start=start):
            queue += f"**{i+1}.** [**{song.source.title}**]({song.source.url})\n"

        embed = discord.Embed(
            description=f"{queue}",
            colour=discord.Colour(0xE9ACFD),
        ).set_footer(text=f"Page {page} of {pages}")
        await ctx.send(embed=embed)

    @commands.command(name="now", aliases=["current", "playing", "nowplaying"])
    async def _now(self, ctx: commands.Context):
        await ctx.send(embed=ctx.voice_state.current.create_embed(), delete_after=60)

    @commands.command(name="remove", aliases=["rem", "delete"])
    async def _remove(self, ctx: commands.Context, index: int):
        if len(ctx.voice_state.songs) == 0:
            return await ctx.send("Empty queue.")

        ctx.voice_state.songs.remove(index - 1)
        await ctx.message.add_reaction("✅")

    # @commands.command(name="progress", aliases=["prog"])
    # async def _progress(self, ctx: commands.Context):
    #     progress = ctx.voice_state.progress()
    #     await ctx.send(progress)

    @_join.before_invoke
    @_play.before_invoke
    async def ensure_voice_state(self, ctx: commands.Context):
        if not ctx.author.voice or not ctx.author.voice.channel:
            raise commands.CommandError("You are not connected to any voice channel.")

        if ctx.voice_client:
            if ctx.voice_client.channel != ctx.author.voice.channel:
                raise commands.CommandError("Bot is already in a voice channel.")


def setup(bot):
    bot.add_cog(Music(bot))
