""" Permission Check Utils
"""
import os
from pymongo import MongoClient


async def has_permission(ctx):
    """ Checks if the author has the required permission to run the command

    Returns:
        bool: Whether the author has permission or not
    """

    if ctx.permissions.administrator is True:
        return True
    if ctx.author.id == 123: # TODO: replace with your ID
        return True

    cluster = MongoClient(os.getenv("MONGODB_URL"))
    database = cluster[str(ctx.guild.id)]
    banned_users = database["Banned"]

    is_banned = banned_users.find_one({"_id": str(ctx.author.id)})

    if is_banned is not None:
        return False

    permissions = database["Permissions"]
    permission_lookup = permissions.find_one({"_id": ctx.command.qualified_name})

    if permission_lookup is None:
        return False

    author_id = str(ctx.author.id)
    author_roles = [str(r.id) for r in ctx.author.roles]

    if "users" not in permission_lookup:
        permission_lookup["users"] = []

    if "roles" not in permission_lookup:
        permission_lookup["roles"] = []

    if author_id not in permission_lookup["users"]:
        db_permissions = [p["id"] for p in permission_lookup["roles"]]

        access = set(author_roles).intersection(set(db_permissions))
        if access == set():
            return False

    return True
