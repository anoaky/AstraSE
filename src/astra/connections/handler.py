import discord

from astra.connections import AstraDBConnection
from astra.generation import AstraMarkovModel

class QuoteView(discord.ui.View):
    
    def __init__(self, interaction: discord.Interaction, target: discord.Member | discord.User, raw: list[tuple[str, int]], perPage: int = 5):
        self.interaction = interaction
        self._raw = raw
        self.total_pages = (len(raw) // perPage) + 1 if (len(raw) % perPage != 0) else (len(raw) // perPage)
        self.page = 1
        self.per_page = perPage
        self.target = target
        super().__init__(timeout=60)
        
    async def show(self):
        embed = await self.build_view()
        await self.update_buttons()
        await self.interaction.response.send_message(embed=embed, view=self)
        
    async def build_view(self):
        start, end = (self.page - 1) * self.per_page, self.page * self.per_page
        embed = discord.Embed(title=self.target, description='')
        for (msg, ind) in self._raw[start:end]:
            embed.description += f'#{ind}: "{msg}"\n\n'
        embed.set_author(name=f'Requested by {self.interaction.user}')
        embed.set_footer(text=f'Page {self.page} of {self.total_pages}')
        embed.set_thumbnail(url=self.target.display_avatar.url)
        return embed
    
    async def update_view(self, interaction: discord.Interaction):
        embed = await self.build_view()
        await self.update_buttons()
        await interaction.response.edit_message(embed=embed, view=self)
        
    async def update_buttons(self):
        self.children[0].disabled = (self.total_pages == 1 or self.page <= 2)
        self.children[1].disabled = (self.total_pages == 1 or self.page == 1)
        self.children[2].disabled = (self.total_pages == 1 or self.page == self.total_pages)
        self.children[3].disabled = (self.total_pages == 1 or self.page >= self.total_pages - 1)
        
    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        return interaction.user.id == self.interaction.user.id
       
    @discord.ui.button(style=discord.ButtonStyle.secondary, emoji='⏮️')
    async def first(self, interaction: discord.Interaction, button: discord.Button):
        self.page = 1
        await self.update_view(interaction)
    
    @discord.ui.button(style=discord.ButtonStyle.primary, emoji='⏪')
    async def prev(self, interaction: discord.Interaction, button: discord.Button):
        self.page -= 1
        await self.update_view(interaction)
        
    @discord.ui.button(style=discord.ButtonStyle.primary, emoji='⏩')
    async def succ(self, interaction: discord.Interaction, button: discord.Button):
        self.page += 1
        await self.update_view(interaction)
        
    @discord.ui.button(style=discord.ButtonStyle.secondary, emoji='⏭️')
    async def last(self, interaction: discord.Interaction, button: discord.Button):
        self.page = self.total_pages
        await self.update_view(interaction)
        
    async def on_timeout(self):
        message = await self.interaction.original_response()
        await message.edit(view=None)
    
    

class AstraHandler:
    
    @staticmethod
    async def add_quote(interaction: discord.Interaction, user: discord.Member | discord.User, msg: str):
        if isinstance(msg, discord.Message):
            msg = msg.clean_content
        if await AstraHandler.does_quote_exist(user, msg):
            await interaction.response.send_message('Quote already present.', ephemeral=True)
        else:
            AstraDBConnection().add_quote(user.id, msg)
            await interaction.response.send_message(f'Quoted {user.mention} saying "{msg}"')
            AstraMarkovModel().initialize_model()
        
    @staticmethod
    async def read_quotes(interaction: discord.Interaction, fromUser: discord.Member | discord.User):
        raw = AstraDBConnection.read_quotes(fromUser.id)
        if len(raw) == 0:
            await interaction.response.send_message('No quotes found.', ephemeral=True)
        else:
            view = QuoteView(interaction, fromUser, raw)
            await view.show()
    
    @staticmethod
    async def does_quote_exist(fromUser: discord.Member | discord.User, withMsg: str | discord.Message, /):
        if isinstance(withMsg, discord.Message):
            withMsg = withMsg.clean_content
        result = AstraDBConnection.search_quote(fromUser.id, withMsg)
        print(result)
        return len(result) > 0
    
    @staticmethod
    async def debug_remove_quote(withIdent: int):
        AstraDBConnection.delete_quote(withIdent)