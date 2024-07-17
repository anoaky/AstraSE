﻿import asyncio
import discord

from astra.connections import AstraDBConnection
from astra.exceptions import QuoteAddError
from astra.generation import AstraMarkovModel
from astra.ui import QuoteView, JarView
from valx import detect_profanity

numbers = [
    '0️⃣',
    '1️⃣',
    '2️⃣',
    '3️⃣',
    '4️⃣',
    '5️⃣',
    '6️⃣',
    '7️⃣',
    '8️⃣',
    '9️⃣'
]

class AstraHandler:
    
    @staticmethod
    async def add_quote(interaction: discord.Interaction, user: discord.Member | discord.User, msg: str):
        if isinstance(msg, discord.Message):
            msg = msg.clean_content
        if await AstraHandler.does_quote_exist(user, msg):
            await interaction.response.send_message('Quote already present.', ephemeral=True)
        else:
            try:
                new_id = AstraDBConnection().add_quote(user.id, msg)
                await interaction.response.send_message(f'Added #{new_id} {user.mention}: "{msg}"')
                AstraMarkovModel().initialize_model()
            except QuoteAddError:
                await interaction.response.send_message(f'Failed to add quote; database issue likely.', ephemeral=True)
        
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
        profanity_count = detect_profanity([forMsg.clean_content])
        print(profanity_count)
        if profanity_count > 0:
            AstraDBConnection.incr_jar(forUser=forMsg.author.id, byAmount=profanity_count)
            reacts = []
            n = profanity_count
            while n > 9:
                last_digit = n % 10
                reacts.insert(-1, numbers[last_digit])
                n = n // 10
            reacts.insert(-1, numbers[n])
            for react in reacts:
                await forMsg.add_reaction(react)
                await asyncio.sleep(0.5)
            
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