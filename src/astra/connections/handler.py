import discord
import profanity_check

from astra.connections import AstraDBConnection
from astra.generation import AstraMarkovModel
from astra.base import AbstractPageView

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
            view = QuoteView(interaction=interaction, target=fromUser, raw=raw)
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
        
    @staticmethod
    async def check_profanity(forMsg: discord.Message):
        if profanity_check.predict([forMsg.clean_content])[0] == 1:
            AstraDBConnection.incr_jar(forMsg.author.id)
            await forMsg.add_reaction('🪙')
            
    @staticmethod
    async def jar_check(interaction: discord.Interaction, forUser: discord.Member):
        coins = AstraDBConnection.get_jar(forUser.id)
        if forUser.id == interaction.user.id:
            await interaction.response.send_message(f'You have {coins} :coin: in your jar!')
        else:
            await interaction.response.send_message(f'{forUser.mention} has {coins} :coin: in their jar!', allowed_mentions=discord.AllowedMentions.none())
    
    @staticmethod
    async def show_leaderboard(interaction: discord.Interaction):
        members = [m.id for m in interaction.guild.members]
        list = AstraDBConnection.query_leaderboard(members)
        if len(list) == 0:
            await interaction.response.send_message('No swears in this server, yet.', ephemeral=True)
        else:
            await JarView(interaction=interaction, raw=list).show()