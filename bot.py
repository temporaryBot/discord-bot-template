""" Discord Bot initialization
"""
import asyncio
import logging
import logging.handlers
import os

from discord import Intents
from discord.ext import commands
from dotenv import load_dotenv
load_dotenv()

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
logging.getLogger('discord.http').setLevel(logging.INFO)

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
logging.getLogger('discord.http').setLevel(logging.INFO)

async def main() -> None:
    """ Instantiates the loggers and bot
    """
    file_handler = logging.handlers.RotatingFileHandler(
        filename="logs/discord_bot.log",
        encoding="utf-8",
        maxBytes= 1 * 1024 * 1024,
        backupCount=128,
    )
    terminal_handler = logging.StreamHandler()

    dt_fmt = '%Y-%m-%d %H:%M:%S'
    formatter = logging.Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', dt_fmt, style='{')

    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Comment out when doing local development, it's to display in docker
    terminal_handler.setFormatter(formatter)
    logger.addHandler(terminal_handler)

    intents = Intents.default()
    intents.message_content = True
    intents.members = True
    intents.guilds = True
    intents.guild_typing = True

    bot = commands.Bot(command_prefix='!', intents=intents)

    for file_name in os.listdir("./cogs"):
        if file_name.endswith(".py"):
            print("loading", file_name[:-3])
            await bot.load_extension(f"cogs.{file_name[:-3]}")
    await bot.start(os.getenv("DISCORD_TOKEN"))

asyncio.run(main())
