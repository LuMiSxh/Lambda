__author__ = "Luca Michael Schmidt"
__version__ = "1.00"

# Import
import os
import discord
from discord.ext import commands
import Framework


# Setup


def Presence(Output: str):
    State = Framework.YAML.GET("Client", "Status")
    choice = "ONLINE" if State == 1 else "WARTUNG"
    choicemessage = "(λx.M[x]) → (λy.M[y])" if State == 1 else "Maintenance Mode"
    choicestatus = discord.Status.online if State == 1 else discord.Status.do_not_disturb

    return choice if Output == "choice" else (choicemessage if Output == "choicemessage" else choicestatus)


# Client Setup


intents = discord.Intents.all()
intents.members = True
client = commands.AutoShardedBot(command_prefix=Framework.YAML.GET("Client", "Prefix"),
                                 intents=intents, case_insensitive=True,
                                 activity=discord.Game(Presence("choicemessage")), status=Presence("choicestatus"))


class NewHelp(commands.MinimalHelpCommand):
    def get_command_signature(self, command):
        return '`%s%s %s`' % (self.clean_prefix, command.qualified_name, command.signature)

    async def send_pages(self):
        destination = self.get_destination()
        for page in self.paginator.pages:
            emby = discord.Embed(description=page, colour=Framework.Colour.Orange)
            try:
                await destination.send(embed=emby, delete_after=25)
            except:
                continue


    async def send_command_help(self, command):
        embed = discord.Embed(title=self.get_command_signature(command))
        embed.add_field(name="Help", value=self.get_command_signature(command))
        alias = command.aliases
        if alias:
            embed.add_field(name="Aliases", value=", ".join(alias), inline=False)

        channel = self.get_destination()
        try:
            await channel.send(embed=embed, delete_after=25)
        except:
            return


client.help_command = NewHelp()


# Setup


def Initialize():
    for filename in os.listdir('Cogs'):

        if os.path.isfile(f"Cogs/{filename}"):
            if filename.endswith(".py") and not filename.startswith("__") and not filename.endswith(".pyc"):
                try:
                    client.load_extension(f'Cogs.{filename[:-3]}')
                    print(f"Loaded Cog: |{filename}|")
                except Exception as e:
                    print(f"ERROR Loading Cog: |{filename}| ; Error: |{e.__context__}|")
                    continue
        else:
            for filename2 in os.listdir(f"Cogs/{filename}"):
                if filename2.endswith(".py") and not filename2.startswith("__") and not filename2.endswith(".pyc"):
                    try:
                        client.load_extension(f'Cogs.{filename}.{filename2[:-3]}')
                        print(f"Loaded Cog: |{filename}.{filename2}|")
                    except Exception as e:
                        print(f"ERROR Loading Cog: |{filename}.{filename2}| ; Error: |{e.__context__}|")
                        continue


Initialize()


@client.listen()
async def on_ready():
    print(f"\nState: |{Presence('choice')}| ; Logged in as: |{client.user}| ; Latency: |{client.latency}|\n")



# Token / RUN


client.run(Framework.YAML.TOKEN())
