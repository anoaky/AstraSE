import discord
import discord.ext.commands as commands
import discord.app_commands as app_commands

from database import AstraDBConnection
from data import *
from groups import *

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot('!', intents=intents)

async def command_setup():
    print('Resyncing commands...')
    await bot.add_cog(DebugGroup(bot))
    await bot.add_cog(QuoteGroup(bot))
    await bot.tree.sync()
    print('Done!')

def is_mom():
    def predicate(ctx):
        return ctx.message.author.id == MOM
    return commands.check(predicate)

@bot.event
async def setup_hook():
    await command_setup()

@bot.event
async def on_ready():
    AstraDBConnection()
    print('Ready to go!')
    
@bot.command()
@is_mom()
async def force_resync(ctx):
    await command_setup()
        
@bot.tree.command(description='Version, changelog, and other info')
async def info(interaction: discord.Interaction):
    await interaction.response.send_message(
        """
        **ASTRA: SE**
        A Simple Text Recording Assistant: Slash Edition v1.1

        **New features:**
        - QUOTE GENERATION IS **BACK**. Run `/quote gen` to EXPERIENCE THE MAGIC.

        **NB:** Currently being hosted on my PC, so will probably go offline at times. Do not be alarmed, for She will Return.""", ephemeral=True)

bot.run(TOKEN)