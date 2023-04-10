""" Util Cog
"""
import os
import discord

from discord.ext.commands import Cog, command, is_owner


class Util(Cog):
    """ Handles the utils, like banning from using commands
    """
    def __init__(self, bot):
        self.bot = bot

    @command(name="reload", aliases=["r"])
    @is_owner()
    async def reload(self, ctx) -> None:
        for file_name in os.listdir("./cogs"):
            if file_name.endswith(".py"):
                await self.bot.unload_extension(f"cogs.{file_name[:-3]}")
                await self.bot.load_extension(f"cogs.{file_name[:-3]}")
        
async def setup(bot) -> None:
    """ Setup for the Util Cog
    """
    await bot.add_cog(Util(bot))
