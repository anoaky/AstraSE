import discord
from astra.ui import AbstractPageView

class QuoteView(AbstractPageView):
    
    def __init__(self, *, interaction: discord.Interaction, target: discord.Member, raw: list[tuple[str, int]], perPage: int=5):
        self.target = target
        super().__init__(interaction=interaction, raw=raw, perPage=perPage)
        
    async def build_view(self):
        start, end = (self.page - 1) * self.per_page, self.page * self.per_page
        embed = discord.Embed(title=self.target, description='')
        for (msg, ind) in self._raw[start:end]:
            embed.description += f'#{ind}: "{msg}"\n\n'
        embed.set_author(name=f'Requested by {self.interaction.user}')
        embed.set_footer(text=f'Page {self.page} of {self.total_pages}')
        embed.set_thumbnail(url=self.target.display_avatar.url)
        return embed