# Import
from discord.ext import commands


# Cog Initialising


class Control(commands.Cog):
    def __init__(self, client):
        self.client = client


# Cog Finishing


def setup(client):
    client.add_cog(Control(client))
