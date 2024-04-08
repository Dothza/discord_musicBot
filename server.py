import asyncio
import discord
from discord.ext import commands
import logging

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="$", intents=intents)


class DiscordPlay(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="play_audio")
    async def music(self, ctx, url):
        await ctx.send("Команда получена")


bot = commands.Bot(command_prefix='!#', intents=intents)

TOKEN = "BOTTOKEN"


async def main():
    await bot.add_cog(DiscordPlay(bot))
    await bot.start(TOKEN)


asyncio.run(main())
