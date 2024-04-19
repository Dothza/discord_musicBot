# НЕ ЗАБЫВАЙТЕ УДАЛИТЬ ТОКЕН


import asyncio
import discord
import discord.message
from download import download
from discord.ext import commands
import logging
from discord.utils import get

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="$", intents=intents)


class DiscordPlay(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="play_audio")
    async def music(self, ctx, url):
        await download(url)
        await ctx.channel.send("Спасибо за сообщение")


bot = commands.Bot(command_prefix='!#', intents=intents)

TOKEN = "BOT_TOKEN"


async def main():
    await bot.add_cog(DiscordPlay(bot))
    await bot.start(TOKEN)


asyncio.run(main())
