import os
import discord
import asyncio
import astra

async def add_groups(bot):
    groups = [
        astra.groups.DebugGroup(bot),
        astra.groups.QuoteGroup(bot)
    ]
    async with asyncio.TaskGroup() as tg:
        for grp in groups:
            tg.create_task(bot.add_cog(grp))

if __name__ == '__main__':
    token = os.environ.get('TOKEN')
    intents = discord.Intents.default()
    intents.message_content = True
    bot = astra.Astra('!', intents=intents)
    asyncio.run(add_groups(bot))
    bot.run(token)