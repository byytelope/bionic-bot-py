import asyncio
import logging
import os
import pathlib

import discord
from discord.ext import commands
from dotenv import load_dotenv  # type: ignore

load_dotenv()

logger = logging.getLogger("discord")
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")
handler.setFormatter(logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s"))
logger.addHandler(handler)


class BionicBot(commands.Bot):
    def __init__(self) -> None:
        super().__init__(command_prefix="$", intents=discord.Intents.all())


bot = BionicBot()


async def main() -> None:
    for file in pathlib.Path("cogs").glob("**/[!_]*.py"):
        cog_name = file.parts[1].removesuffix(".py")
        ext = ".".join(file.parts).removesuffix(".py")

        try:
            await bot.load_extension(ext)
            print(f"Successfully loaded cog: {cog_name}")
        except Exception:
            print(f"Failed to load cog: {ext}")

    try:
        await bot.start(token=str(os.getenv("BOT_TOKEN")))
    except KeyboardInterrupt:
        await bot.close()
    finally:
        print("Bot offline.")


if __name__ == "__main__":
    asyncio.run(main())
