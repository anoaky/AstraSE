import discord
import discord.ext.commands as commands
import discord.app_commands as app_commands

from data import *
from handler import AstraHandler, QuoteView

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot('!', intents=intents)

def is_mom():
    def predicate(ctx):
        return ctx.message.author.id == 188832409737756675
    return commands.check(predicate)

@bot.event
async def setup_hook():
    await bot.tree.sync()

@bot.event
async def on_ready():
    print('Ready to go!')
    
@bot.command()
@is_mom()
async def force_resync(ctx):
    print('Resync in progress...')
    await bot.tree.sync()
    print('Done!')
    
@bot.tree.context_menu(name='Quote Message')
async def quote_msg_ctx(interaction: discord.Interaction, msg: discord.Message):
    await AstraHandler.add_quote(msg.author, msg)
    await interaction.response.send_message(f'Quoted {msg.author.mention} saying "{msg.clean_content}"', ephemeral=False)
    
@bot.tree.context_menu(name='Show Quotes')
async def show_quotes_ctx(interaction: discord.Interaction, user: discord.Member):
    raw = await AstraHandler.read_quotes(user)
    if len(raw) == 0:
        await interaction.response.send_message('No quotes found.', ephemeral=True)
    else:
        view = QuoteView(interaction, user, raw)
        await view.show()
        
@bot.tree.command(description='Add a quote')
@app_commands.describe(user='The user to quote')
@app_commands.describe(msg='The quote to add')
async def quote(interaction: discord.Interaction, user: discord.Member, msg: str):
    await AstraHandler.add_quote(user, msg)
    await interaction.response.send_message(f'Quoted {user.mention} saying "{msg}"')
    
@bot.tree.command(description='List quotes')
@app_commands.describe(user='The user to query')
async def list(interaction: discord.Interaction, user: discord.Member):
    # this could be done better
    raw = await AstraHandler.read_quotes(user)
    if len(raw) == 0:
        await interaction.response.send_message('No quotes found.', ephemeral=True)
    else:
        view = QuoteView(interaction, user, raw)
        await view.show()
        
@bot.tree.command(description='Version, changelog, and other info')
async def info(interaction: discord.Interaction):
    await interaction.response.send_message(
        """
        **ASTRA: SE**
        A Simple Text Recording Assistant: Slash Edition v1.0

        **New features:**
        - Slash commands! Use `/quote` and `/list` to manually add and list quotes
        - Context commands! Right-click on a message, then go to Apps > Add Quote to quickly add a quote from a Discord message. Similarly, right-click on a user and go to Apps > Show Quotes to show a user's quotes.

        **NB:** Currently being hosted on my PC, so will probably go offline at times. Do not be alarmed, for She will Return.""", ephemeral=True)

bot.run(TOKEN)