# Import
import discord
from discord.ext import commands
import asyncio
import youtube_dl
import Framework


# Optionen bestimmung


ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


# YTDLSource Class


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data
        self.title = data.get('title')
        self.url = data.get('url')
        self.thumbnail = data.get('thumbnail')


    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

# Cog Initialising


class MUSIK(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.queue = {}


    @commands.command()
    async def join(self, ctx, *, channel: discord.VoiceChannel):

        if ctx.voice_client is not None:
            self.queue = {}
            return await ctx.voice_client.move_to(channel)
        self.queue = {}
        await channel.connect()


    @commands.command()
    async def play(self, ctx, *, url):
        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.client.loop, stream=True)

        if len(self.queue) == 0:

            self.start_playing(ctx.voice_client, player)
            embed = discord.Embed(
                title='',
                colour=Framework.Colour.Musik,
                description=f'[{format(player.title)}]({player.url})'
            )
            embed.set_author(name='Now playing:')
            embed.set_image(url=player.thumbnail)
            embed.set_footer(text=f'Added by: {ctx.author.name}', icon_url=ctx.author.avatar_url)
            embed.set_thumbnail(url=Framework.YAML.GET("Pictures", "Accept"))

            await Framework.Messaging.Universal_send(ctx, embed, 35)

        else:

            self.queue[len(self.queue)] = player
            embed = discord.Embed(
                title='',
                colour=Framework.Colour.Musik,
                description=f'[{format(player.title)}]({player.url})'
            )
            embed.set_author(name='Added to queue:')
            embed.set_image(url=player.thumbnail)
            embed.set_footer(text=f'Added by: {ctx.author.name}', icon_url=ctx.author.avatar_url)
            embed.set_thumbnail(url=Framework.YAML.GET("Pictures", "Accept"))

            await Framework.Messaging.Universal_send(ctx, embed, 35)

        try:
            while ctx.voice_client.is_connected():
                await asyncio.sleep(3)
                if len(ctx.voice_client.channel.members) == 1:
                    await ctx.voice_client.disconnect()
                    break
                elif ctx.voice_client.is_paused():
                    await asyncio.sleep(3)
                elif ctx.voice_client.is_playing():
                    await asyncio.sleep(3)
                else:
                    await ctx.voice_client.disconnect()
                    break
        except:
            return


    def start_playing(self, voice_client, player):

        self.queue[0] = player

        i = 0
        while i < len(self.queue):
            try:
                voice_client.play(self.queue[i], after=lambda e: print('Player error: %s' % e) if e else None)

            except:
                pass
            i += 1


    @commands.command(aliases=["v"])
    async def volume(self, ctx, volume: float):

        if ctx.voice_client is None:

            embed = discord.Embed(
                title=f'{Framework.YAML.GET("Embed", "Help")}',
                colour=Framework.Colour.Error,
                description='Im not connected to a voice channel!'
            )
            embed.set_thumbnail(url=Framework.YAML.GET("Pictures", "Animated", "Error"))

            return await Framework.Messaging.Universal_send(ctx, embed, 15)

        elif ctx.voice_client is not None:

            ctx.voice_client.source.volume = volume / 100

            embed = discord.Embed(
                title='Volume',
                colour=Framework.Colour.Musik,
                description=f'Set volume to: `{volume}`%'
            )
            embed.set_footer(text=f"Adjusted by: {ctx.author.name}", icon_url=ctx.author.avatar_url)
            embed.set_thumbnail(url=Framework.YAML.GET("Pictures", "Accept"))

            return await Framework.Messaging.Universal_send(ctx, embed, 15)


    @commands.command()
    async def stop(self, ctx):

        try:
            await ctx.voice_client.disconnect()
            await ctx.message.delete()
        except:
            try:
                await ctx.message.delete()
            except:
                pass


    @commands.command()
    async def pause(self, ctx):

        if ctx.voice_client.is_playing():

            ctx.voice_client.pause()
            await ctx.message.delete()
            return
        try:
            await ctx.message.delete()
        except:
            pass


    @commands.command()
    async def resume(self, ctx):

        if ctx.voice_client.is_paused():

            ctx.voice_client.resume()
            await ctx.message.delete()
            return

        try:
            await ctx.message.delete()
        except:
            pass


    @play.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            self.queue = {}
            if ctx.author.voice:
                try:
                    await ctx.author.voice.channel.connect()
                except:
                    pass
            else:
                return


# Cog Finishing


def setup(client):
    client.add_cog(MUSIK(client))
