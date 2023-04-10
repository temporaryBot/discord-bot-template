""" Permissions Cog
"""
import os

from typing import Union

import discord

from discord.ext.commands import Cog, check, group
from prettytable import PrettyTable
from pymongo import MongoClient

from utils.permission_check import has_permission

class Permissions(Cog):
    """ Handles the permissions for commands
    """
    def __init__(self, bot):
        self.bot = bot

        self.cluster = MongoClient(os.getenv("MONGODB_URL"))

    def _extract_command(self, ctx) -> Union[str, None]:
        """ Extracts the command from the double quotes

        Returns:
            str/None: The command or None if not found
        """
        try:
            command = ctx.message.content.split('"')[1::2][0]
        except IndexError:
            return None

        is_command = self.bot.get_command(command)
        if is_command is None:
            return None
        
        return command

    @group(name="permissions", aliases=["p"])
    @check(has_permission)
    async def permissions(self, ctx) -> None:
        """ Base permission command
        """
    
    @permissions.command(name="get", aliases=["g"])
    @check(has_permission)
    async def get_permissions(self, ctx, command) -> None:
        """
        """
        command = self._extract_command(ctx)
        if command is None:
            return

        database = self.cluster[str(ctx.guild.id)]
        permissions = database["Permissions"]
        
        lookup = permissions.find_one({"_id": command})
        if lookup is not None:
            table = PrettyTable()
            table.field_names = ["type", "name", "nickname", "id"]

            if "users" in lookup:
                for user in lookup["users"]:
                    table.add_row(["user", user["name"], user["nickname"], user["id"]])

            if "roles" in lookup:
                for role in lookup["roles"]:
                    table.add_row(["role", role["name"], "", role["id"]])

            await ctx.send(f"Permissions for the !{command}\n```\n{table}\n```")
    
    @permissions.command(name="reset", aliases=["rst"])
    @check(has_permission)
    async def reset_permissions(self, ctx, command) -> None:
        """
        """
        command = self._extract_command(ctx)
        if command is None:
            return
        
        database = self.cluster[str(ctx.guild.id)]
        permissions = database["Permissions"]

        lookup = permissions.find_one({"_id": command})
        if lookup is not None:
            permissions.delete_one({"_id": command})

    @permissions.group(name="set", aliases=["s"])
    @check(has_permission)
    async def set_permissions(self, ctx, command) -> None:
        """ Base set command
        """

    @set_permissions.group(name="add", aliases=["a"])
    @check(has_permission)
    async def add_permissions(self, ctx) -> None:
        """ Base add command
        """

    @add_permissions.command(name="users", aliases=["u"])
    @check(has_permission)
    async def add_users(self, ctx, users) -> None:
        """
        """
        command = self._extract_command(ctx)
        if command is None:
            return
        
        database = self.cluster[str(ctx.guild.id)]
        permissions = database["Permissions"]

        users = [user.strip() for user in users.split(",")]
        for user in users:
            try:
                fetched_user = await ctx.guild.fetch_member(int(user))
            except (discord.NotFound, TypeError):
                continue

            entry = {
                "id": str(fetched_user.id),
                "nickname": fetched_user.display_name,
                "name": str(fetched_user)
            }
            action = {
                "$addToSet": {
                    "users": {
                        "$each": [entry]
                    }
                }
            }
            
            permissions.update_one({"_id": command}, action, upsert=True)

    @add_permissions.command(name="roles", aliases=["r"])
    @check(has_permission)
    async def add_roles(self, ctx, roles) -> None:
        """
        """
        command = self._extract_command(ctx)
        if command is None:
            return
        
        database = self.cluster[str(ctx.guild.id)]
        permissions = database["Permissions"]

        roles = [role.strip() for role in roles.split(",")]
        server_roles = await ctx.guild.fetch_roles()
        for role in roles:
            role_match = next((r for r in server_roles if role in (r.name.lower(), str(r.id)) or "everyone" in role), None)
            if role_match is None:
                continue

            entry = {
                "id": str(role_match.id),
                "name": role_match.name
            }
            action = {
                "$addToSet": {
                    "roles": {
                        "$each": [entry]
                    }
                }
            }

            permissions.update_one({"_id": command}, action, upsert=True)
    
    @set_permissions.group(name="remove", aliases=["rm"])
    @check(has_permission)
    async def remove_permissions(self, ctx) -> None:
        """ Base remove command
        """

    @remove_permissions.command(name="users", aliases=["u"])
    @check(has_permission)
    async def remove_users(self, ctx, users: str) -> None:
        """
        """
        command = self._extract_command(ctx)
        if command is None:
            return

        # Avoids regex for any number of spaces in-between
        users = [user.strip() for user in users.split(",")]

        database = self.cluster[str(ctx.guild.id)]
        permissions = database["Permissions"]

        command_lookup = permissions.find_one({"_id": command})
        if command_lookup is None:
            return

        for user in users:
            match_condition = {
                "users": {
                    "$elemMatch": {
                        "$or": [
                            {"id": user},
                            {"name": user},
                            {"nickname": user}
                        ]
                    }
                }
            }
            user_lookup = permissions.find_one(match_condition)
            if user_lookup is None:
                return
            
            user_match = [u["id"] for u in user_lookup["users"] if user in (u["id"], u["name"], u["nickname"])][0]
            permissions.update_one({"_id": command}, {"$pull": {"users": {"id": user_match}}})

    @remove_permissions.command(name="roles", aliases=["r"])
    @check(has_permission)
    async def remove_roles(self, ctx, roles) -> None:
        """
        """
        command = self._extract_command(ctx)
        if command is None:
            return

        # Avoids regex for any number of spaces in-between
        roles = [role.strip() for role in roles.split(",")]

        database = self.cluster[str(ctx.guild.id)]
        permissions = database["Permissions"]

        command_lookup = permissions.find_one({"_id": command})
        if command_lookup is None:
            return

        for role in roles:
            role = f"@{role}" if role == "everyone" else role

            match_condition = {
                "roles": {
                    "$elemMatch": {
                        "$or": [
                            {"id": role},
                            {"name": role}
                        ]
                    }
                }
            }
            role_lookup = permissions.find_one(match_condition)
            if role_lookup is None:
                return
            
            role_match = [r["id"] for r in role_lookup["roles"] if role in (r["id"], r["name"])][0]
            print(role_match)
            permissions.update_one({"_id": command}, {"$pull": {"roles": {"id": role_match}}})
        
async def setup(bot) -> None:
    """ Setup for the Permissions Cog
    """
    await bot.add_cog(Permissions(bot))
