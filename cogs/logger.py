""" Logger Cog
"""
import os
import uuid

from datetime import datetime

from discord.ext.commands import Cog
from dotenv import load_dotenv

from pymongo import MongoClient


class Logger(Cog):
    """ Handles the hugging of players
    """
    def __init__(self, bot):
        self.bot = bot

        self.cluster = MongoClient(os.getenv("MONGODB_URL"))

    @Cog.listener()
    async def on_command(self, ctx) -> None:
        """ Logs every command
        """

        guild_id = str(ctx.guild.id)
        database = self.cluster[guild_id]

        if os.getenv(f"{guild_id}-logs") is None:
            parameters = {"capped": True, "size": 1073741824} # 1GB of logs in bytes

            database.create_collection("Logs", **parameters)

            with open(".env", "a", encoding="utf-8") as f:
                f.write(f"{guild_id}-logs=true\n")
            load_dotenv()

        entry = {
            "_id": str(uuid.uuid4()),
            "message": ctx.message.content.strip(),
            "author_name": str(ctx.author),
            "author_id": str(ctx.author.id),
            "timestamp": datetime.utcnow()
        }
        database["Logs"].insert_one(entry)
        
async def setup(bot) -> None:
    """ Setup for the Logger  Cog
    """
    await bot.add_cog(Logger(bot))
