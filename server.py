import asyncio
import discord
import datetime as dt
from discord.ext import commands
import logging

logging.basicConfig(filename="temporary.log")
# TODO: Настроить базовое логирование


intents = discord.Intents.default()
bot = commands.Bot(command_prefix="$", intents=intents)
