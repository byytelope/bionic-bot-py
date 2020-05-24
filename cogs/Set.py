import discord
import psycopg2
from discord.ext import commands

class Set(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.db = psycopg2.connect(
            database="d5gmd9koh5vegt", 
            user="htildhifgbegjh", 
            password="b4b03250555235feb27acab0d9abbf0be289a0b08cc265478be37bcbd87c5c8c", 
            host="ec2-52-202-22-140.compute-1.amazonaws.com", 
            port="5432")
        self.cursor = self.db.cursor()

    @commands.group(invoke_without_command=True)
    async def set(self, ctx):
        embed = discord.Embed(
            title = 'set **<command>**',
            colour = discord.Colour.blurple()
            )
        embed.set_footer(text=f'{ctx.guild}', icon_url=f'{ctx.guild.icon_url}')
        embed.add_field(name='welctext', value='Set welcome text.', inline=False)
        embed.add_field(name='welcch', value='Set welcome channel.', inline=False)

        await ctx.send(embed=embed)

    @set.command(aliases=['welctext'])
    @commands.has_any_role('Chernobyl', 'Three Mile Island')
    async def set_welc_text(self, ctx, *, welc_text):

        audit_ch = self.bot.get_channel(712599778868854794)

        self.cursor.execute('SELECT welc_text FROM main WHERE guild_id = %s', (str(ctx.guild.id)))
        result = self.cursor.fetchone()

        if result is None:
            sql = ('INSERT INTO main (guild_id, welc_text) VALUES(%s, %s)', (str(ctx.guild.id), welc_text))
            await ctx.send(f'''
                Welcome text has been set to **"{welc_text}"**
                ''')

            embed = discord.Embed(
            title=ctx.author,
            description=f'set welcome channel to **"{welc_text}"**',
            colour=discord.Colour.blurple()
            )
            await audit_ch.send(embed=embed)

        elif result is not None:
            sql = ('UPDATE main SET welc_text = %s WHERE guild_id = %s', (welc_text, str(ctx.guild.id)))
            await ctx.send(f'''
                Welcome text has been changed to "{welc_text}"
                ''')

            embed = discord.Embed(
            title=ctx.author,
            description=f'changed welcome text to **"{welc_text}"**',
            colour=discord.Colour.blurple()
            )
            await audit_ch.send(embed=embed)
    
        self.cursor.execute(sql)
        self.db.commit()
        self.cursor.close()
        self.db.close()

    @set.command(aliases=['welcch'])
    @commands.has_any_role('Chernobyl', 'Three Mile Island')
    async def set_welc_ch(self, ctx, welc_ch: discord.TextChannel):
        self.cursor.execute(f'SELECT ch_id_welc FROM main WHERE guild_id = %s', (str(ctx.guild.id)))
        result = self.cursor.fetchone()

        audit_ch = self.bot.get_channel(712599778868854794)

        if result is None:
            sql = ('INSERT INTO main (guild_id, ch_id_welc) VALUES(%s, %s)', (str(ctx.guild.id), welc_ch))
            await ctx.send(f'Welcome channel has been set to {welc_ch.mention}')

            embed = discord.Embed(
            title=ctx.author,
            description=f'set welcome channel to {welc_ch.mention}',
            colour=discord.Colour.blurple()
            )
            await audit_ch.send(embed=embed)

        elif result is not None:
            sql = ('UPDATE main SET ch_id_welc = %s WHERE guild_id = %s', (welc_ch, str(ctx.guild.id)))
            await ctx.send(f'Welcome channel has been changed to {welc_ch.mention}')

            embed = discord.Embed(
            title=ctx.author,
            description=f'changed welcome channel to {welc_ch.mention}',
            colour=discord.Colour.blurple()
            )
            await audit_ch.send(embed=embed)

        self.cursor.execute(sql)
        self.db.commit()
        self.cursor.close()
        self.db.close()


def setup(bot):
    bot.add_cog(Set(bot))