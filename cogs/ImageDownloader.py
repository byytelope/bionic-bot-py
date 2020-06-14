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
        src_path = Path("img_cache/*.jpg")
        disc_file_path = Path("img_cache/image.jpg")

        response = GoogleImagesSearch(os.environ['img_search_api_key'], os.environ['img_search_web_id'])
        args = {'q':key, 'num':1, 'fileType':"jpg"}

        source_name = glob.glob(f"{src_path}")
        if source_name:
            path, fullname = os.path.split(f"{source_name[0]}")
            if fullname == "image.jpg":
                os.remove(f"{source_name}")
                print("Image deleted.")
        else:
            pass

        response.search(search_params=args, path_to_dir=out_dir)

        # path = output[0][args['keywords']][0]

        source_name = glob.glob(f"{src_path}")
        if source_name:
            path, fullname = os.path.split(f"{source_name[0]}")
            basename, ext = os.path.splitext(fullname)
            target_name = os.path.join(path, f'image{ext}')
            os.rename(source_name[0], target_name)
            print(f"Renamed {basename}{ext} to image{ext}.")
        else:
            print("Image not found.")

        file = discord.File(disc_file_path, filename="image.jpg")
        embed = discord.Embed(
            title=key,
            colour=discord.Colour(0xe9acfd)
        )
        embed.set_image(url="attachment://image.jpg")
        embed.set_footer(text=f'Image requested by: {ctx.author}', icon_url=ctx.author.avatar_url)
        await ctx.send(file=file, embed=embed)


def setup(bot):
    bot.add_cog(ImageDownloader(bot))