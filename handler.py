import discord
import asyncio

from database import AstraDBConnection

class QuoteView(discord.ui.View):
    
    def __init__(self, interaction: discord.Interaction, target: discord.Member | discord.User, raw: list[tuple[str, int]], perPage: int = 10):
        self.interaction = interaction
        self._raw = raw
        self.total_pages = (len(raw) // perPage) + 1
        self.page = 1
        self.per_page = perPage
        self.target = target
        super().__init__()
        
    async def show(self):
        embed = await self.build_view()
        await self.update_buttons()
        await self.interaction.response.send_message(embed=embed, view=self)
        
    async def build_view(self):
        start, end = (self.page - 1) * self.per_page, self.page * self.per_page
        embed = discord.Embed(title=self.target, description='')
        for (msg, ind) in self._raw[start:end]:
            if len(msg) > 50:
                msg = msg[0:50] + '...'
            embed.description += f'#{ind}: "{msg}"\n'
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
    async def add_quote(user: discord.Member | discord.User, msg: str | discord.Message):
        loop = asyncio.get_event_loop()
        conn = await loop.run_in_executor(None, AstraDBConnection.__new__, AstraDBConnection)
        if isinstance(msg, discord.Message):
            msg = msg.clean_content
        await loop.run_in_executor(None, conn.add_quote, user.id, msg)
        
    @staticmethod
    async def read_quotes(fromUser: discord.Member | discord.User):
        loop = asyncio.get_event_loop()
        conn = await loop.run_in_executor(None, AstraDBConnection.__new__, AstraDBConnection)
        return await loop.run_in_executor(None, conn.read_quotes, fromUser.id)