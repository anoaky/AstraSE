import discord
import discord.ext.commands as commands
from discord import app_commands

from handler import AstraHandler
from data import *

@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
class DebugGroup(commands.GroupCog, name='debug', group_name='debug'):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        
    @app_commands.command(name='remove', description='Remove a quote')
    @app_commands.describe(ident='ID of quote')
    async def remove_quote(self, interaction: discord.Interaction, ident: int):
        await AstraHandler.debug_remove_quote(ident)
        await interaction.response.send_message('Done!', ephemeral=True)
    
    async def interaction_check(self, interaction: discord.Interaction, /):
        return interaction.user.id == MOM