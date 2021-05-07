# Import
import discord
from discord.ext import commands
from datetime import datetime
import Framework


# Cog Initialising


class Support(commands.Cog):
    def __init__(self, client):
        self.client = client


    # TELL


    @commands.command(aliases=["t"])
    @commands.has_permissions(administrator=True)
    @commands.has_permissions(administrator=True)
    async def tell(self, ctx, *, Nachricht):

        embed = discord.Embed(
            title='',
            colour=discord.Colour.red(),
            description=f'{Nachricht}'
        )

        await ctx.message.delete()
        await ctx.send(embed=embed)


    @commands.command()
    @commands.is_owner()
    async def suptell(self, ctx, user: discord.Member, *, message):

        embed = discord.Embed(
            title="<SUPPORT>",
            colour=discord.Colour.red(),
            description=f"{message}",
            timestamp=datetime.utcnow()
        )
        try:
            await ctx.message.delete()
        except:
            pass
        await user.send(embed=embed)


    @commands.command()
    @commands.has_permissions(administrator=True)
    async def masstell(self, ctx, *, message):

        embed = discord.Embed(
            title="<SUPPORT>",
            colour=discord.Colour.red(),
            description=f"{message}",
            timestamp=datetime.utcnow()
        )
        embed.set_footer(text=f"Mass-messaging by: {ctx.author.name}")


        try:
            await ctx.message.delete()
        except:
            pass

        for user in ctx.guild.members:
            try:
                await user.send(embed=embed)
            except:
                pass


# Cog Finishing


def setup(client):
    client.add_cog(Support(client))
