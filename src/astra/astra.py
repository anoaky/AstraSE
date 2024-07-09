import discord
import discord.ext.commands as commands
import discord.app_commands as app_commands
import sys

from astra.connections import AstraDBConnection, AstraHandler
from astra.groups import *

info_text = """
**ASTRA: SE**
A Simple Text Recording Assistant: Special Edition v1.3.0

**New features:**
- Swear jar! Watch your propfamtiy."""

class Astra(commands.Bot):
    def __init__(self, prefix, **kwargs):
        super().__init__(prefix, **kwargs)
        base_cmds = [
            app_commands.Command(name='info',
                                 description='Version, changelog, and other info',
                                 callback=self.info)
        ]
        for cmd in base_cmds:
            self.tree.add_command(cmd)
        
    async def setup_hook(self) -> None:
        await super().setup_hook()
        AstraDBConnection.initialize()
        await self.tree.sync()
        
    async def on_ready(self):
        print('ready', file=sys.stderr)
        
    async def on_message(self, message):
        await AstraHandler.check_profanity(message)
        
    async def info(self, interaction: discord.Interaction):
        await interaction.response.send_message(info_text, ephemeral=True)