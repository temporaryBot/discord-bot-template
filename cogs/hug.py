""" Hug Cog
"""
import discord

from discord.ext.commands import Cog, check, command, parameter

from utils.permission_check import has_permission


class Hug(Cog):
    """ Handles the hugging of players
    """
    def __init__(self, bot):
        self.bot = bot

    @command(name="hug")
    @check(has_permission)
    async def hug(self, ctx, *,member: discord.Member = parameter(description=" - Someone who needs a hug")) -> None:
        await ctx.send(f"{ctx.author.display_name} hugged {member.display_name}")
        
async def setup(bot) -> None:
    """ Setup for the Hug  Cog
    """
    await bot.add_cog(Hug(bot))
