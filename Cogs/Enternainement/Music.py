# Import
import DiscordUtils
import discord
from discord.ext import commands
import Framework


# Cog Initialising


class MUSIK(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.music = DiscordUtils.Music()


    @commands.command()
    async def play(self, ctx, *, url):
        player = self.music.get_player(guild_id=ctx.guild.id)
        if not player:
            player = self.music.create_player(ctx, ffmpeg_error_betterfix=True)

        if not ctx.voice_client.is_playing() or not ctx.voice_client.is_paused:

            await player.queue(url, search=True)

            song = await player.play()

            embed = discord.Embed(
                title='',
                colour=Framework.Colour.Musik,
                description=f'[{Framework.safe_format(song.name)}]({song.url})'
            )
            embed.set_author(name='Now Playing:')
            embed.set_image(url=song.thumbnail)
            embed.set_footer(text=f'Added by: {ctx.author.name}', icon_url=ctx.author.avatar_url)
            embed.set_thumbnail(url=self.client.user.avatar_url)

            await Framework.Messaging.Universal_send(ctx, embed, 15)

        else:

            song = await player.queue(url, search=True)
            embed = discord.Embed(
                title='',
                colour=Framework.Colour.Musik,
                description=f'[{Framework.safe_format(song.name)}]({song.url})'
            )
            embed.set_author(name='Added to Queue:')
            embed.set_image(url=song.thumbnail)
            embed.set_footer(text=f'Added by: {ctx.author.name}', icon_url=ctx.author.avatar_url)
            embed.set_thumbnail(url=self.client.user.avatar_url)

            await Framework.Messaging.Universal_send(ctx, embed, 15)

        try:
            while ctx.voice_client.is_connected():
                if len(ctx.voice_client.channel.members) == 1:
                    await player.disable()
                    await ctx.voice_client.disconnect()
                    break
                elif ctx.voice_client.is_paused():
                    pass
                elif ctx.voice_client.is_playing():
                    pass
                else:
                    await player.disable()
                    await ctx.voice_client.disconnect()
                    break
        except:
            try:
                await ctx.voice_client.disconnect()
                await player.disable()
            except:
                return



    @commands.command()
    async def stop(self, ctx):
        player = self.music.get_player(guild_id=ctx.guild.id)
        if player:
            await player.stop()
            await ctx.message.delete()
            return
        try:
            await ctx.message.delete()
        except:
            return



    @commands.command()
    async def resume(self, ctx):
        if ctx.voice_client.is_paused():
            player = self.music.get_player(guild_id=ctx.guild.id)
            await player.resume()
            await ctx.message.delete()
        else:

            embed = discord.Embed(
                title=f'{Framework.YAML.GET("Embed", "Help")}',
                colour=Framework.Colour.Musik,
                description='Music not paused!'
            )
            embed.set_thumbnail(url=self.client.user.avatar_url)

            await Framework.Messaging.Universal_send(ctx, embed)
            return


    @commands.command()
    async def pause(self, ctx):
        if ctx.voice_client.is_playing():
            player = self.music.get_player(guild_id=ctx.guild.id)
            await player.pause()
            await ctx.message.delete()
        else:

            embed = discord.Embed(
                title=f'{Framework.YAML.GET("Embed", "Help")}',
                colour=Framework.Colour.Musik,
                description='Music already paused!'
            )
            embed.set_thumbnail(url=self.client.user.avatar_url)

            await Framework.Messaging.Universal_send(ctx, embed, 15)



    @commands.command()
    async def leave(self, ctx):
        player = self.music.get_player(guild_id=ctx.guild.id)
        if player:
            await player.disable()
            await ctx.voice_client.disconnect()
        await ctx.message.delete()


    @commands.command()
    async def skip(self, ctx):
        player = self.music.get_player(guild_id=ctx.guild.id)

        if player:

            data = await player.skip(force=True)

            embed = discord.Embed(
                title='',
                colour=Framework.Colour.Musik,
                description=f'[{Framework.safe_format(data[1].name)}]({data[1].url})'
            )
            embed.set_author(name='Skipped:')
            embed.set_image(url=data[1].thumbnail)
            embed.set_footer(text=f'Skipped by: {ctx.author.name}', icon_url=ctx.author.avatar_url)
            embed.set_thumbnail(url=self.client.user.avatar_url)

            await Framework.Messaging.Universal_send(ctx, embed, 15)
            return
        try:
            await ctx.message.delete()
        except:
            return


    @commands.command(aliases=["v"])
    async def volume(self, ctx, vol: float):
        player = self.music.get_player(guild_id=ctx.guild.id)
        if player:
            song, volume = await player.change_volume(float(vol) / 10)

            embed = discord.Embed(
                title='Volume',
                colour=Framework.Colour.Musik,
                description=f'Volume for **{Framework.safe_format(song.name)}** set to **{(volume * 10)}**%.'
            )
            embed.set_footer(text=f"Adjusted by: {ctx.author.name}", icon_url=ctx.author.avatar_url)
            embed.set_thumbnail(url=self.client.user.avatar_url)

            return await Framework.Messaging.Universal_send(ctx, embed, 15)
        try:
            await ctx.message.delete()
        except:
            return


    @commands.command()
    async def queue(self, ctx):
        x = 1
        player = self.music.get_player(guild_id=ctx.guild.id)

        if player:

            embed = discord.Embed(
                title='',
                colour=Framework.Colour.Musik
            )
            embed.set_author(name='Queue:')
            embed.set_thumbnail(url=self.client.user.avatar_url)

            for song in player.current_queue():
                embed.add_field(name=f"-<{x}>-", value=f"{song.name}")
                x += 1

            await Framework.Messaging.Universal_send(ctx, embed, 15)
            return
        try:
            await ctx.message.delete()
        except:
            return


    @commands.command()
    async def remove(self, ctx, index: int):
        player = self.music.get_player(guild_id=ctx.guild.id)
        if player:
            song = await player.remove_from_queue(int(index))

            embed = discord.Embed(
                title='',
                colour=Framework.Colour.Musik,
                description=f"**{song.name}** removed from Queue"
            )
            embed.set_author(name='Queue:')
            embed.set_thumbnail(url=self.client.user.avatar_url)

            await Framework.Messaging.Universal_send(ctx, embed, 15)
            return
        try:
            await ctx.message.delete()
        except:
            return


    @commands.command()
    async def loop(self, ctx):
        player = self.music.get_player(guild_id=ctx.guild.id)

        if player:
            song = await player.toggle_song_loop()
            if song.is_looping:
                await Framework.Messaging.Universal_send(ctx, f"Loop for Track: **{song.name}** active.")
            else:
                await Framework.Messaging.Universal_send(ctx, f"Loop for Track: **{song.name}** inactive.")
        try:
            await ctx.message.delete()
        except:
            return


    @play.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                try:
                    await ctx.author.voice.channel.connect()
                except:
                    return
        else:
            pass


# Cog Finishing


def setup(client):
    client.add_cog(MUSIK(client))
