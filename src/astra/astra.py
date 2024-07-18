import discord
import discord.ext.commands as commands
import discord.app_commands as app_commands
import sys

from astra.connections import AstraDBConnection, AstraHandler
from astra.groups import *

class Astra(commands.Bot):
        
    async def setup_hook(self) -> None:
        await super().setup_hook()
        AstraDBConnection.initialize()
        await self.tree.sync()
        
    async def on_ready(self):
        print('ready', file=sys.stderr)
        
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return
        else:
            await AstraHandler.check_profanity(message)