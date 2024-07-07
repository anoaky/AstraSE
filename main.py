import os
import discord
import asyncio
import astra

if __name__ == '__main__':
    token = os.environ.get('TOKEN')
    intents = discord.Intents.default()
    intents.message_content = True
    bot = astra.Astra('!', intents=intents)
    asyncio.run(bot.add_cog(astra.groups.DebugGroup(bot)))
    asyncio.run(bot.add_cog(astra.groups.QuoteGroup(bot)))
    bot.run(token)