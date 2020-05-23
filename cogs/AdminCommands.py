import discord
import random
from discord.ext import commands

class AdminCommands(commands.Cog):
    """
    Admin commands for admins
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['clear'])
    @commands.has_any_role('Chernobyl', 'Three Mile Island')
    @commands.has_permissions(manage_messages=True)
    async def cls(self, ctx, amount=3):
        embed = discord.Embed(
            title=ctx.author,
            description=f'cleared **{amount}** message(s) in {ctx.channel.mention}',
            colour=discord.Colour.blurple()
        )
        audit_ch = self.bot.get_channel(712599778868854794)

        await ctx.channel.purge(limit=amount)
        await ctx.channel.send(f"Aju {amount} message delete kollin.")
        await audit_ch.send(embed=embed)

    @cls.error
    async def on_cls_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions) or isinstance(error, commands.MissingAnyRole):
            responses = ['Adhi the command beynun vey varah ekalo bondo nivei.',
                         'Hoho kanthethi.'
                        ]
            await ctx.send(random.choice(responses))
      
    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, user: discord.Member, *,reason=None):
        embed = discord.Embed(
            title=f'**{ctx.author}** kicked **{user}** from bionic.',
            description=reason,
            colour=discord.Colour.blurple()
            )
        audit_ch = self.bot.get_channel(712599778868854794)
        
        await user.kick(reason=reason)
        await ctx.send(f'Bye bye **{user.mention}**.')
        await audit_ch.send(embed=embed)

    # @kick.error
    # async def on_kick_error(self, ctx, error):
    #     if isinstance(error, commands.MissingPermissions):
    #         responses = ['Adhi the command beynun vey varah ekalo bondo nivei.',
    #                         'Hoho kanthethi.'
    #                     ]
    #         await ctx.send(random.choice(responses))

    @commands.command(aliases=['reqinv'])
    async def req_invite(self, ctx):
        admin_ch = self.bot.get_channel(712447089623171104)
        global inv_author
        inv_author = ctx.author
        global auth_ch
        auth_ch = ctx.channel

        await ctx.channel.send(f'Requesting invite link from admins...')
        await admin_ch.send(f'{inv_author.mention} is requesting an invite link for {ctx.channel.mention}. Use .confirm **no. of uses** or .deny')
    
    @commands.command()
    @commands.has_any_role('Chernobyl', 'Three Mile Island')
    async def confirm(self, ctx, i=5):
        link = await ctx.channel.create_invite(max_age=86400, max_uses=i)
        dm = self.bot.get_user(inv_author.id)
        embed = discord.Embed(
            title=f'**{ctx.author}** confirmed an invite link request.',
            description=f'from **{inv_author}** for {auth_ch.mention}',
            colour=discord.Colour.blurple()
            )
        audit_ch = self.bot.get_channel(712599778868854794)

        await dm.send(f'{link}')
        await auth_ch.send(f'Invite link requested by {inv_author.mention} was confirmed. Pls check your dms for the link.')
        await audit_ch.send(embed=embed)

    @commands.command()
    @commands.has_any_role('Chernobyl', 'Three Mile Island')
    async def deny(self, ctx):
        embed = discord.Embed(
            title=f'**{ctx.author}** denied an invite link request.',
            description=f'from **{inv_author}** for {auth_ch.mention}',
            colour=discord.Colour.blurple())
        audit_ch = self.bot.get_channel(712599778868854794)

        await auth_ch.send(f"Invite link requested by {inv_author.mention} was denied.")
        await audit_ch.send(embed=embed)


def setup(bot):
    bot.add_cog(AdminCommands(bot))