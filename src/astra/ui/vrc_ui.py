import discord

from astra.connections import VRChatConnector

class PlayerSearchView(discord.ui.view):
    def __init__(self, *, interaction: discord.Interaction):
        self.interaction = interaction
        super().__init__(timeout=60)
        
    async def build_view(self):
        self.search_box = discord.ui.TextInput(
            label='Search',
            placeholder='Enter a username',
            callback=self.search_callback
        )
        self.dropdown = discord.ui.Select(disabled=True)
        self.add_item(self.search_box).add_item(self.dropdown)
        
    async def show(self):
        embed = discord.Embed(title='VRChat Player Search')
        await self.build_view()
        await self.interaction.response.send_message(embed=embed, view=self)
        
    async def update_dropdown(self, txt: list[str]):
        for t in txt:
            self.dropdown.add_option(label=t)
        self.dropdown.disabled = False
    
    async def dropdown_callback(self, interaction: discord.Interaction):
        await interaction.response.edit_message(content=f'Selected {self.dropdown.values[0]}')
        
    async def search_callback(self, interaction: discord.Interaction):
        tm = self.search_box.value
        res = await VRChatConnector.search_user(search=tm)
        await self.update_dropdown([u.display_name for u in res])