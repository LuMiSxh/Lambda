# Import
import asyncio
import datetime
import random
import discord
from discord.ext import commands
import Framework


# Cog Initialising


class EVENT(commands.Cog):

    def __init__(self, client):
        self.client = client


    # CLIENT JOIN


    @commands.Cog.listener()
    async def on_guild_join(self, guild):

        embed = discord.Embed(
            title='Hello!',
            colour=Framework.Colour.Green,
            description=f'Thanks for adding me to your Server!\nLets get startet, use: `{self.client.command_prefix}help` for command usage.'
        )
        embed.add_field(name='**help**', value='Zeigt dir die Commands.')
        embed.set_thumbnail(url=self.client.user.avatar_url)

        await guild.text_channels[0].send(embed=embed)


    @commands.Cog.listener()
    async def on_message(self, message):

        if not message.guild:
            return

        elif message.author.bot:
            return

        if message.content.startswith("<<help"):
            await asyncio.sleep(0.5)
            try:
                await message.delete()
            except:
                pass

        elif f'<@!{self.client.user.id}>' or f'<@{self.client.user.id}>' in message.content:
            m = await message.channel.send(
                f'Hello! Since you pinged me, I assume that you forgot my Prefix, which is: `{self.client.command_prefix}`')
            await asyncio.sleep(60)
            await m.delete()
            return


# Cog Finishing


def setup(client):
    client.add_cog(EVENT(client))
