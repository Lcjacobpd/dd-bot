import os
import discord
from dotenv import load_dotenv
from enum import Enum


"""
SETTINGS
"""

#region Discord Variables

load_dotenv()
API_TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID_INT = int(os.getenv("GUILD_ID"))
GUILD_ID = discord.Object(id=GUILD_ID_INT)

PARENT_ID = os.getenv("PARENT_ID")

#endregion

#region Custom Discord Emojis

class CustomEmoji:
    #Copy the ID from discord to add your own
    heyo  = "<:heyo:829028736162201700>"
    nat1  = "<:nat1:818628379967356960>"
    nat20 = "<:nat20:818628403119783957>"

    d2_emojis = {
        "glimmer"           : "<:d2_material_glimmer:1042134639969566750>",
        "vanguard tokens"   : "<:d2_faction_vanguard:1042948486875856949>",
        "crucible tokens"   : "<:d2_faction_crucible:1042948478134923407>",
        "cryptarch tokens"  : "<:d2_faction_cryptarch:1042948479686819930>"
    }

#endregion

#region Inventory Variables

DATA_FILE = "data.json"
TRACKED_ITEMS = [
    "glimmer",
    "varguard tokens",
    "crucible tokens",
    "cryptarch tokens"
]
class InventoryAction(Enum):
    Add = 1
    Subtract = 2
    Total = 3

#endregion

#region Dice Roll Variables

ROLL_COMMAND_PATTERN = r"r(?P<count>[1-9]?\d*)?d(?P<di>[1-9]\d*)(?P<modifier>(?:[\-\+][1-9]\d*)?)(?P<roll_type>(?:ad|wd)?)"
class RollType(Enum):
    Normal = 1
    Advantage = 2
    Disadvantage = 3

#endregion