import discord

from discord import app_commands

class AGroup(app_commands.Group):
    def __init__(self, /, *, menus: list[app_commands.ContextMenu], cmds: list[app_commands.Command], tree: app_commands.CommandTree, parent: app_commands.Group, **kwargs):
        super().__init__(**kwargs)
        self.menus = menus
        self.cmds = cmds
        self.tree = tree
        self.parent = parent
        
        for cmd in self.cmds:
            self.add_command(cmd)
        for menu in self.menus:
            self.tree.add_command(menu)
        