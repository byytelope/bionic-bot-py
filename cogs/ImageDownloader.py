import discord
import glob
import os
from discord.ext import commands
from google_images_search import GoogleImagesSearch
from pathlib import Path

class ImageDownloader(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def img(self, ctx, *, key):
        await ctx.send("Aju photo ah hoadhaathaan...")

        out_dir = Path("img_cache")
        src_path = Path("img_cache/*")

        response = GoogleImagesSearch(os.environ['img_search_api_key'], os.environ['img_search_web_id'])
        args = {'q':key, 'num':1, 'fileType':"jpg|png"}

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
        if source_name:
            path, fullname = os.path.split(f"{source_name[0]}")
            basename, ext = os.path.splitext(fullname)
            target_name = os.path.join(path, f'image{ext}')
            os.rename(source_name[0], target_name)
            print(f"Renamed {basename}{ext} to image{ext}.")
        else:
            print("File not found.")

        embed = discord.Embed(
            title=key,
            colour=discord.Colour(0xe9acfd)
        )
        embed.set_footer(text=f'Image requested by: {ctx.author}', icon_url=ctx.author.avatar_url)
        if ext == ".jpg":
            embed.set_image(url="attachment://image.jpg")
            file = discord.File("img_cache/image.jpg", filename="image.jpg")
        elif ext == ".png":
            embed.set_image(url="attachment://image.png")
            file = discord.File("img_cache/image.png", filename="image.png")
        elif ext == ".gif":
            embed.set_image(url="attachment://image.gif")
            file = discord.File("img_cache/image.gif", filename="image.gif")

        await ctx.send(file=file, embed=embed)

    @commands.command()
    async def gif(self, ctx, *, key):
        await ctx.send("Aju gif ah hoadhaathaan...")

        out_dir = Path("img_cache")
        src_path = Path("img_cache/*")

        response = GoogleImagesSearch(os.environ['img_search_api_key'], os.environ['img_search_web_id'])
        args = {'q':key, 'num':1, 'fileType':"gif"}

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
        if source_name:
            path, fullname = os.path.split(f"{source_name[0]}")
            basename, ext = os.path.splitext(fullname)
            if ext == ".gif":
                target_name = os.path.join(path, f'image{ext}')
                os.rename(source_name[0], target_name)
                print(f"Renamed {basename}{ext} to image{ext}.")
            else:
                print("Gif not found.")
        else:
            print("File not found.")

        embed = discord.Embed(
            title=key,
            colour=discord.Colour(0xe9acfd)
        )
        embed.set_footer(text=f'Gif requested by: {ctx.author}', icon_url=ctx.author.avatar_url)
        embed.set_image(url="attachment://image.gif")
        file = discord.File("img_cache/image.gif", filename="image.gif")

        await ctx.send(file=file, embed=embed)


def setup(bot):
    bot.add_cog(ImageDownloader(bot))