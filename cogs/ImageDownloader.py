import discord
import glob
import os
from discord.ext import commands
from google_images_download import google_images_download
from pathlib import Path

class ImageDownloader(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def img(self, ctx, *, key):
        await ctx.send("Aju photo ah hoadhaathaan...")

        out_dir = Path('cogs/img_cache')
        src_path = Path("cogs/img_cache/*.jpg")
        disc_file_path = Path("cogs/img_cache/image.jpg")

        response = google_images_download.googleimagesdownload()
        args = {'keywords':key, 'limit':1, 'print_urls':True, 'no_directory':True, 'output_directory':out_dir, 'format':"jpg"}

        source_name = glob.glob(f"{src_path}")
        if source_name:
            path, fullname = os.path.split(f"{source_name[0]}")
            if fullname == "image.jpg":
                os.remove(f"{source_name}")
                print("Image deleted.")
        else:
            pass

        output = response.download(args)
        print(output)

        # path = output[0][args['keywords']][0]

        source_name = glob.glob(f"{src_path}")
        if source_name:
            path, fullname = os.path.split(f"{source_name[0]}")
            basename, ext = os.path.splitext(fullname)
            target_name = os.path.join(path, f'image{ext}')
            os.rename(source_name, target_name)
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