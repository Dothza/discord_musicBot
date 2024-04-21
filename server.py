# НЕ ЗАБЫВАЙТЕ УДАЛИТЬ ТОКЕН


import asyncio
import discord
import discord.message
from data.download import download
from discord.ext import commands
import logging
from discord.utils import get
from data import db_session

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

db_session.global_init("db/songs.db")

intents = discord.Intents.all()


class DiscordPlay(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="info")
    async def help(self, ctx):
        await ctx.channel.send(
            "Музыкальный бот Discord\nКоманда $play - включить песню\nКоманда $stop - остановить воспроизведение.")

    @commands.command(name="play")
    async def music(self, ctx, url):
        channel = ctx.message.author.voice.channel
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect(reconnect=True, timeout=None)
        await download(url)
        await ctx.channel.send(f"{queue['title']} - воспроизводится.")


    async def play(self, song, voice):
        await voice.play(discord.FFmpegPCMAudio(song["url"], executable="data/ffmpeg.exe"))
        return song

    @commands.command(name="stop")
    async def stop_music(self, ctx):
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        voice.stop()
        await ctx.channel.send("Воспроизведение остановлено.")

    @commands.command(name="kick")
    @commands.has_permissions(administration=True)
    async def kick(self, ctx, membre: discord.Member, *, reason=None):
        await ctx.channel.purge(limit=1)
        await membre.kick(reason=reason)


TOKEN = "TOKEN"

bot = commands.Bot(command_prefix="$", intents=intents)


async def main():
    await bot.add_cog(DiscordPlay(bot))
    await bot.start(TOKEN)


asyncio.run(main())
