# Import
import discord
import aiohttp
from discord.ext import commands
from discord import Webhook, AsyncWebhookAdapter
import traceback
from datetime import datetime
import Framework


# Cog Initialising


class Error(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.ignored = [commands.CommandNotFound, commands.DisabledCommand]
        self.Normal = [AttributeError, ArithmeticError, OSError, FileNotFoundError, IndentationError, IndexError,
                       ImportError, SyntaxError, TypeError, Framework.YAMLError]

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):

        try:
            typ = type(error.original)
        except:
            typ = type(error)

        print(typ)

        if typ in self.ignored:
            return

        if typ in self.Normal:
            # Error Code Chinchilla
            embed = discord.Embed(
                title=f"{Framework.YAML.GET('Embed', 'Help')}",
                colour=Framework.Colour.Error,
                description=f"Error Code: `Chinchilla`.\nException:\n`{error}`",
                timestamp=datetime.utcnow()
            )
            embed.set_thumbnail(url=Framework.YAML.GET("Pictures", "Animated", "Error"))

            await Framework.Messaging.Universal_send(ctx, embed, 15)
            return


        if isinstance(typ, commands.BadArgument or commands.BadBoolArgument or commands.TooManyArguments or commands.MissingRequiredArgument):
            # Error Code Rabbit
            embed = discord.Embed(
                title=f"{Framework.YAML.GET('Embed', 'Help')}",
                colour=Framework.Colour.Error,
                description=f"Error Code: `Rabbit`.\nException:\n`{error}`",
                timestamp=datetime.utcnow()
            )
            embed.set_thumbnail(url=Framework.YAML.GET("Pictures", "Animated", "Error"))

            await Framework.Messaging.Universal_send(ctx, embed, 15)
            return

        if isinstance(typ, commands.BotMissingAnyRole or commands.BotMissingPermissions or commands.MissingPermissions or commands.MissingAnyRole):
            # Error Code Baboon
            embed = discord.Embed(
                title=f"{Framework.YAML.GET('Embed', 'Help')}",
                colour=Framework.Colour.Error,
                description=f"Error Code: `Baboon`.\nException:\n`{error}`",
                timestamp=datetime.utcnow()
            )
            embed.set_thumbnail(url=Framework.YAML.GET("Pictures", "Animated", "Error"))

            await Framework.Messaging.Universal_send(ctx, embed, 15)
            return

        elif isinstance(typ, commands.ChannelNotFound or commands.ChannelNotReadable or commands.GuildNotFound or discord.NotFound or discord.GatewayNotFound):
            # Error Code Elephant
            embed = discord.Embed(
                title=f"{Framework.YAML.GET('Embed', 'Help')}",
                colour=Framework.Colour.Error,
                description=f"Error Code: `Elephant`.\nException:\n`{error}`",
                timestamp=datetime.utcnow()
            )
            embed.set_thumbnail(url=Framework.YAML.GET("Pictures", "Animated", "Error"))

            await Framework.Messaging.Universal_send(ctx, embed, 15)
            return

        elif isinstance(typ, commands.MissingAnyRole or commands.MissingPermissions or commands.CommandOnCooldown):
            # Error Code Orphan
            embed = discord.Embed(
                title=f"{Framework.YAML.GET('Embed', 'Help')}",
                colour=Framework.Colour.Error,
                description=f"Error Code: `Orphan`.\nException:\n`{error}`",
                timestamp=datetime.utcnow()
            )
            embed.set_thumbnail(url=Framework.YAML.GET("Pictures", "Animated", "Error"))

            await Framework.Messaging.Universal_send(ctx, embed, 15)
            return

        else:

            async with aiohttp.ClientSession() as session:
                url = Framework.YAML.GET("Client", "WebHook", "System")

                webhook = Webhook.from_url(url, adapter=AsyncWebhookAdapter(session))

                trace = traceback.format_exception(None, error, error.__traceback__)
                if '\nThe above exception was the direct cause of the following exception:\n\n' in trace:
                    trace = trace[:trace.index(
                        '\nThe above exception was the direct cause of the following exception:\n\n')]
                traceback_text = "\n".join(trace)

                try:
                    Server = ctx.guild.name
                except:
                    Server = None
                try:
                    Channel = ctx.channel.name
                except:
                    Channel = None

                embed = discord.Embed(
                    title="An Exception occurred!",
                    colour=Framework.Colour.Error,
                    description=f"**Used by:**\n`{ctx.author} | {ctx.author.id}`\n\n"
                                f"**Command information:**\n"
                                f"Executed on Server: `{Server}`\n"
                                f"Executed in Channel: `{Channel}`\n"
                                f"Cog: `{ctx.cog}`\n"
                                f"Command: `{self.client.command_prefix}{ctx.command.name} {ctx.command.signature}`\n"
                                f"_Executed:_ `{ctx.message.content}`\n\n"
                                f"**Error:**\n"
                                f"`{error}`\n\n"
                                f"**Traceback:**```py\n{str(traceback_text)}\n```",
                    timestamp=datetime.utcnow()
                )
                embed.set_thumbnail(url=Framework.YAML.GET("Pictures", "Animated", "Error"))

                await webhook.send(username="System Notification", avatar_url=self.client.user.avatar_url, embed=embed)

                # Error Code Hate
                embed = discord.Embed(
                    title=f"{Framework.YAML.GET('Embed', 'Exception')}",
                    colour=Framework.Colour.Error,
                    description=f"Error Code: `Hate`.\nException:\n`{error}`",
                    timestamp=datetime.utcnow()
                )
                embed.set_thumbnail(url=Framework.YAML.GET("Pictures", "Animated", "Error"))

                await Framework.Messaging.Universal_send(ctx, embed, 15)


# Cog Finishing


def setup(client):
    client.add_cog(Error(client))
