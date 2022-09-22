import asyncio
import logging
import os
import pathlib
from typing import Any

import discord
import pymongo
from discord.ext import commands
from dotenv import load_dotenv  # type: ignore

load_dotenv()

logger = logging.getLogger("discord")
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")
handler.setFormatter(
    logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s")
)
logger.addHandler(handler)


class BionicBot(commands.Bot):
    def __init__(self) -> None:
        super().__init__(command_prefix="$", intents=discord.Intents.all())

    async def setup_hook(self) -> None:
        client = pymongo.MongoClient(
            str(os.getenv("DB_URL")), document_class=dict[str, Any]
        )

        try:
            client.server_info()
            print("Connected to MongoDB")
        except Exception:
            print("Couldn't connect to MongoDB")

        self.db = client.bionic_bot_py

        # await self.db.execute(
        #     """
        #     CREATE TABLE IF NOT EXISTS guilds
        #     (
        #         id bigint PRIMARY KEY,
        #         ch_id_welcome bigint,
        #         ch_id_logs bigint
        #     );
        #     """
        # )

        print(f"\nLogged in as: {self.user}")
        return await super().setup_hook()


async def main() -> None:
    bot = BionicBot()

    for file in pathlib.Path("cogs").glob("**/[!_]*.py"):
        cog_name = file.parts[1].removesuffix(".py")
        ext = ".".join(file.parts).removesuffix(".py")

        try:
            await bot.load_extension(ext)
            print(f"Successfully loaded cog: {cog_name}")
        except Exception:
            print(f"Failed to load cog: {ext}")

    try:
        await bot.start(str(os.getenv("BOT_TOKEN")))
    except KeyboardInterrupt:
        await bot.close()
        print("Bot offline.")


if __name__ == "__main__":
    asyncio.run(main())
