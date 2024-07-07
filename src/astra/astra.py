import discord
import discord.ext.commands as commands
import discord.app_commands as app_commands
import sys

from astra.connections import AstraDBConnection
from astra.groups import *

class Astra(commands.Bot):
    def __init__(self, prefix, **kwargs):
        super().__init__(prefix, **kwargs)
        
    async def setup_hook(self) -> None:
        await super().setup_hook()
        AstraDBConnection.initialize()
        await self.tree.sync()
        
    async def on_ready(self):
        print('ready', file=sys.stderr)
        
    @app_commands.command(description='Version, changelog, and other info')
    async def info(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            """
            **ASTRA: SE**
            A Simple Text Recording Assistant: Slash Edition v1.2

            **New features:**
            - QUOTE GENERATION IS **BACK**. Run `/quote gen` to EXPERIENCE THE MAGIC.""", ephemeral=True)