import discord
import glob
import os
from discord.ext import commands
from google_images_download import google_images_download

class ImageDownloader(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def img(self, ctx, *, key):
        await ctx.send("Aju photo ah hoadhaathaan...")
        response = google_images_download.googleimagesdownload()
        args = {'keywords':key, 'limit':1, 'print_urls':True, 'no_directory':True, 'output_directory':'aju-bot-py\\img_cache', 'format':"jpg"}

        source_name = glob.glob("aju-bot-py\\img_cache\\*.jpg")[0]
        path, fullname = os.path.split(source_name)

        if fullname == "image.jpg":
            os.remove(source_name)
            print("Image deleted.")

        output = response.download(args)
        print(output)

        # path = output[0][args['keywords']][0]

        source_name = glob.glob("aju-bot-py\\img_cache\\*.jpg")[0]
        path, fullname = os.path.split(source_name)
        basename, ext = os.path.splitext(fullname)
        target_name = os.path.join(path, f'image{ext}')
        os.rename(source_name, target_name)

        print(f"Renamed {basename}{ext} to image{ext}.")

        file = discord.File("aju-bot-py\\img_cache\\image.jpg", filename="image.jpg")
        embed = discord.Embed(
            title=key,
            colour=discord.Colour(0xe9acfd)
        )
        embed.set_image(url="attachment://image.jpg")
        embed.set_footer(text=f'Image requested by: {ctx.author}', icon_url=ctx.author.avatar_url)
        await ctx.send(file=file, embed=embed)


def setup(bot):
    bot.add_cog(ImageDownloader(bot))