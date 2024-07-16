import discord
from astra.ui import AbstractPageView

class JarView(AbstractPageView):
    
    def __init__(self, *, interaction: discord.Interaction, raw: list[tuple[int, int]], perPage: int=10):
        super().__init__(interaction=interaction, raw=raw, perPage=perPage)
        
    async def build_view(self):
        start, end = (self.page - 1) * self.per_page, self.page * self.per_page
        embed = discord.Embed(title=f'{self.interaction.guild.name} Leaderboard', description='**Showing the top 20**\n')
        for (id, count) in self._raw[start:end]:
            embed.description += f'\n{self.interaction.guild.get_member(id).display_name}: {count} 🪙\n'
        embed.set_author(name=f'Requested by {self.interaction.user}')
        embed.set_footer(text=f'Page {self.page} of {self.total_pages}')
        embed.set_thumbnail(url=(self.interaction.guild.icon.url if self.interaction.guild.icon is not None else None))
        return embed
