# НЕ ЗАБЫВАЙТЕ УДАЛИТЬ ТОКЕН


import asyncio
import discord
import discord.message
from data.download import download
from discord.ext import commands
import logging
from discord.utils import get

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

intents = discord.Intents.all()


class DiscordPlay(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="play")
    async def music(self, ctx, url):
        channel = ctx.message.author.voice.channel
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()
        voice.play(discord.FFmpegPCMAudio(await download(url), executable="data/ffmpeg.exe"))
        await ctx.channel.send("Песня воспроизводится.")


TOKEN = "BOTTOKEN"

bot = commands.Bot(command_prefix="$", intents=intents)


async def main():
    await bot.add_cog(DiscordPlay(bot))
    await bot.start(TOKEN)

asyncio.run(main())
