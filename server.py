# НЕ ЗАБЫВАЙТЕ УДАЛИТЬ ТОКЕН


import asyncio
import logging
import os
import random
import discord
import discord.message
from data.download import download
from discord.ext import commands
from discord.utils import get
from data import db_session
from data.db_session import *
from data.song import Song

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

intents = discord.Intents.all()
try:
    os.remove("db/base.db")
except FileNotFoundError:
    pass
finally:
    db_session.global_init("db/base.db")


class DiscordPlay(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.current_song = None

    @commands.command(name="play")
    async def music(self, ctx, url):
        channel = ctx.message.author.voice.channel
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        await download(url)
        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect(reconnect=True, timeout=None)
        await self.start_song()
        voice.play(discord.FFmpegPCMAudio(self.current_song.link, executable="data/ffmpeg.exe"))
        await ctx.channel.send(f"{self.current_song.name} - воспроизводится.")

    async def start_song(self):
        db_session = create_session()
        if self.current_song:
            self.current_song = db_session.query(Song).filter(Song.id == self.current_song.id + 1)[0]
        else:
            self.current_song = db_session.query(Song).filter(Song.id == 1)[0]

    @commands.command(name="skip")
    async def skip_song(self, ctx):
        db_session = create_session()
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        if self.current_song:
            try:
                self.current_song = db_session.query(Song).filter(Song.id == self.current_song.id + 1)[0]
            except IndexError:
                await ctx.channel.send("Очередь пуста.")
        else:
            self.current_song = db_session.query(Song).filter(Song.id == 1)[0]
        if voice.is_playing:
            voice.stop()
            voice.play(discord.FFmpegPCMAudio(self.current_song.link, executable="data/ffmpeg.exe"))
            await ctx.channel.send(f"{self.current_song.name} - воспроизводится.")

    @commands.command(name="info")
    async def help(self, ctx):
        await ctx.channel.send(
            "Музыкальный бот Discord\nКоманда $play - включить песню\nКоманда $stop - остановить воспроизведение.")

    @commands.command(name="stop")
    async def stop_music(self, ctx):
        db_session = create_session()
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        if voice:
            voice.stop()
            await ctx.channel.send("Воспроизведение остановлено.")
        else:
            await ctx.channel.send("Ничего не проигрывается.")
        db_session.query(Song).delete()
        db_session.commit()

    @commands.command(name="pause")
    async def pause_music(self, ctx):
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        if voice:
            voice.pause()
            await ctx.channel.send("Воспроизведение приостановлено.")
        else:
            await ctx.channel.send("Ничего не проигрывается.")

    @commands.command(name="resume")
    async def resume_music(self, ctx):
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        if voice and voice.is_paused():
            voice.resume()
            await ctx.channel.send("Воспроизведение возобновлено.")
        else:
            await ctx.channel.send("Ничего не проигрывается.")

    @commands.command(name="kick")
    @commands.has_permissions(administrator=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        await ctx.channel.purge(limit=1)
        await member.kick(reason=reason)
        await ctx.channel.send(f"{member} был кикнут с сервера.")

    @commands.command(name="joke")
    async def rickroll(self, ctx):
        channel = ctx.message.author.voice.channel
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        queue = await download("https://youtu.be/dQw4w9WgXcQ?si=NcPkSTzU4pe7SDsv")
        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect(reconnect=True, timeout=None)
        voice.play(discord.FFmpegPCMAudio(queue, executable="data/ffmpeg.exe"))
        await ctx.channel.send("You have been rickrolled :)")

    @commands.command(name="game")
    async def game(self, ctx, cards_col):
        cards = {"черви_6": 6, "черви_7": 7, "черви_8": 8, "черви_9": 9, "черви_10": 10, "черви_валет": 1,
                 "черви_дама": 2, "черви_kороль": 3, "черви_туз": 11,
                 "крести_6": 6, "крести_7": 7, "крести_8": 8, "крести_9": 9, "крести_10": 10, "крести_валет": 1,
                 "крести_дама": 2, "крести_kороль": 3, "крести_туз": 11,
                 "буби_6": 6, "буби_7": 7, "буби_8": 8, "буби_9": 9, "буби_10": 10, "буби_валет": 1, "буби_дама": 2,
                 "буби_kороль": 3, "буби_туз": 11,
                 "пики_6": 6, "пики_7": 7, "пики_8": 8, "пики_9": 9, "пики_10": 10, "пики_валет": 1, "пики_дама": 2,
                 "пики_kороль": 3, "пики_туз": 11}
        players_cards = []
        players_points = 0
        bots_points = 0
        bots_cards = []
        cards_col = int(cards_col)
        if 0 < int(cards_col) <= 5:
            for i in range(cards_col):
                card = random.choice(list(cards.keys()))
                players_points += cards[card]
                players_cards.append(card)
            for i in range(random.randint(1, 4)):
                card = random.choice(list(cards.keys()))
                bots_points += cards[card]
                bots_cards.append(card)
            if players_points > 21:
                await ctx.channel.send("Перебор")
                await ctx.channel.send(f"Ваши карты: {players_cards}")
            elif bots_points > 21 >= players_points:
                await ctx.channel.send("Вы выиграли")
                await ctx.channel.send(f"Ваши карты: {players_cards}")
                await ctx.channel.send(f"Карты бота: {bots_cards}")
            elif bots_points <= players_points < 21:
                await ctx.channel.send("Вы выиграли")
                await ctx.channel.send(f"Ваши карты: {players_cards}")
                await ctx.channel.send(f"Карты бота: {bots_cards}")
            elif 21 >= bots_points > players_points:
                await ctx.channel.send("Вы проиграли")
                await ctx.channel.send(f"Ваши карты: {players_cards}")
                await ctx.channel.send(f"Карты бота: {bots_cards}")
        else:
            await ctx.channel.send("Неподходящее число")


TOKEN = "BOT_TOKEN"

bot = commands.Bot(command_prefix="$", intents=intents)


async def main():
    await bot.add_cog(DiscordPlay(bot))
    await bot.start(TOKEN)


asyncio.run(main())
