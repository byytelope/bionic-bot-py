import glob
import os
from pathlib import Path

import discord
from discord.ext import commands
from google_images_search import GoogleImagesSearch


class ImageDownloader(commands.Cog):
    """
    Class for dowloading images
    """

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command()
    async def img(self, ctx: commands.Context, *, query: str) -> None:
        await ctx.send("Aju photo ah hoadhaathaan...")

        out_dir = Path("img_cache")
        src_path = Path("img_cache/*")

        response = GoogleImagesSearch(os.environ["IMG_SEARCH_API_KEY"], os.environ["IMG_SEARCH_WEB_ID"])
        args = {"q": query, "num": 1, "fileType": "jpg|png"}

        source_name = glob.glob(f"{src_path}")
        if source_name:
            path, fullname = os.path.split(f"{source_name[0]}")
            if "image" in fullname:
                os.remove(f"{source_name[0]}")
                print("File deleted.")
        else:
            pass

        response.search(search_params=args, path_to_dir=out_dir)

        source_name = glob.glob(f"{src_path}")
        embed: discord.Embed = None
        file: discord.File = None

        if source_name:
            path, fullname = os.path.split(f"{source_name[0]}")
            basename, ext = os.path.splitext(fullname)
            target_name = os.path.join(path, f"image{ext}")
            os.rename(source_name[0], target_name)
            print(f"Renamed {basename}{ext} to image{ext}.")

            embed = discord.Embed(title=query, colour=discord.Colour(0xE9ACFD))
            embed.set_footer(text=f"Image requested by: {ctx.author}", icon_url=ctx.author.avatar_url)

            if ext == ".jpg":
                embed.set_image(url="attachment://image.jpg")
                file = discord.File("img_cache/image.jpg", filename="image.jpg")
            elif ext == ".png":
                embed.set_image(url="attachment://image.png")
                file = discord.File("img_cache/image.png", filename="image.png")
        else:
            print("File not found.")
        try:
            await ctx.send(file=file, embed=embed)
        except Exception as e:
            print(f"Error sending image: {e}")

    # @commands.command()
    # async def gif(self, ctx: commands.Context, *, query: str) -> None:
    #     await ctx.send("Aju gif ah hoadhaathaan...")

    #     out_dir = Path("img_cache")
    #     src_path = Path("img_cache/*")

    #     response = GoogleImagesSearch(os.environ["IMG_SEARCH_API_KEY"], os.environ["IMG_SEARCH_WEB_ID"])
    #     args = {"q": query, "num": 1, "fileType": "gif"}

    #     source_name = glob.glob(f"{src_path}")
    #     if source_name:
    #         path, fullname = os.path.split(f"{source_name[0]}")
    #         if "image" in fullname:
    #             os.remove(f"{source_name[0]}")
    #             print("File deleted.")
    #     else:
    #         pass

    #     response.search(search_params=args, path_to_dir=out_dir)

    #     source_name = glob.glob(f"{src_path}")
    #     if source_name:
    #         path, fullname = os.path.split(f"{source_name[0]}")
    #         basename, ext = os.path.splitext(fullname)
    #         if ext == ".gif":
    #             target_name = os.path.join(path, f"image{ext}")
    #             os.rename(source_name[0], target_name)
    #             print(f"Renamed {basename}{ext} to image{ext}.")
    #         else:
    #             print("Gif not found.")
    #     else:
    #         print("File not found.")

    #     embed = discord.Embed(title=query, colour=discord.Colour(0xE9ACFD))
    #     embed.set_footer(text=f"Gif requested by: {ctx.author}", icon_url=ctx.author.avatar_url)
    #     embed.set_image(url="attachment://image.gif")
    #     file = discord.File("img_cache/image.gif", filename="image.gif")

    #     try:
    #         await ctx.send(file=file, embed=embed)
    #     except Exception as e:
    #         print(e)


def setup(bot) -> None:
    bot.add_cog(ImageDownloader(bot))
