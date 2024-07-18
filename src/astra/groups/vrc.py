import discord
import discord.ext.commands as commands
import discord.app_commands as app_commands

def nsfw_check():
    def predicate(interaction: discord.Interaction) -> bool:
        return interaction.channel.is_nsfw()
    return app_commands.check(predicate)

class VRCGroup(commands.GroupCog, name='vrc', group_name='vrc'):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    
    