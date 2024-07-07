import argparse
import asyncio
import discord
import discord.ext.commands as commands
import discord.app_commands as app_commands

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
        print('Ready!')
        
    @app_commands.command(description='Version, changelog, and other info')
    async def info(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            """
            **ASTRA: SE**
            A Simple Text Recording Assistant: Slash Edition v1.2

            **New features:**
            - QUOTE GENERATION IS **BACK**. Run `/quote gen` to EXPERIENCE THE MAGIC.""", ephemeral=True)
        
if __name__ == '__main__':
    def main():
        parser = argparse.ArgumentParser()
        parser.add_argument('token')
        args = parser.parse_args()
    
        intents = discord.Intents.default()
        intents.message_content = True
        astra = Astra('!', intents=intents)
        asyncio.run(astra.add_cog(DebugGroup(astra)))
        asyncio.run(astra.add_cog(QuoteGroup(astra)))
        astra.run(args.token)
        
    main()