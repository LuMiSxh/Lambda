# Import
import asyncio
import discord
from discord.ext import commands
from datetime import datetime
import Framework


# Cog Initialising


class Guild(commands.Cog):
    def __init__(self, client):
        self.client = client


    # BAN


    @commands.command()
    @commands.has_permissions(administrator=True)
    @commands.cooldown(5, 120, commands.BucketType.guild)
    async def ban(self, ctx, user: discord.Member, *, reason="Keinen Grund angegeben."):

        embed = discord.Embed(
            title=f'Es gibt einen Rebellenspion in unserer Mitte... {user.name}...',
            colour=discord.Colour.red(),
            timestamp=datetime.utcnow()
        )
        embed.add_field(name='**User:**', value=f'{user.mention}')
        embed.add_field(name='**Reason:**', value=f'{reason}')
        embed.add_field(name='**By:**', value=f'{ctx.author.mention}')
        embed.set_thumbnail(url=self.client.user.avatar_url)

        await ctx.message.delete()
        m = await ctx.send(embed=embed)
        await user.send(embed=embed)
        await user.ban(reason=reason)
        await asyncio.sleep(15)
        await m.delete()


    # KICK


    @commands.command()
    @commands.has_permissions(administrator=True)
    @commands.cooldown(5, 120, commands.BucketType.guild)
    async def kick(self, ctx, user: discord.Member, *, reason="No reason provided."):

        embed = discord.Embed(
            title=f"{user.name}, you were everything but not innocent...",
            colour=discord.Colour.red(),
            timestamp=datetime.utcnow()
        )
        embed.add_field(name='**User:**', value=f'{user.mention}')
        embed.add_field(name='**Reason:**', value=f'{reason}')
        embed.add_field(name='**By:**', value=f'{ctx.author.mention}')
        embed.set_thumbnail(url=self.client.user.avatar_url)

        await ctx.message.delete()
        m = await ctx.send(embed=embed)
        await user.send(embed=embed)
        await user.kick(reason=reason)
        await asyncio.sleep(15)
        await m.delete()

    # CLEAR

    @commands.command(aliases=["c"])
    @commands.has_permissions(administrator=True)
    @commands.cooldown(2, 60, commands.BucketType.user)
    async def clear(self, ctx, Anzahl: int = None):
        x = 0

        for _ in await ctx.channel.purge(limit=Anzahl):
            x += 1

        embed = discord.Embed(
            title='Messages cleared!',
            colour=Framework.Colour.Green,
            description=f'`{x}` Messages deleted.',
        timestamp=datetime.utcnow()
        )
        embed.set_thumbnail(url=Framework.YAML.GET("Pictures", "Accept"))

        await Framework.Messaging.Universal_send(ctx, embed)


# Cog Finishing


def setup(client):
    client.add_cog(Guild(client))
