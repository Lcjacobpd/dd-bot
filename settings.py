import os
import discord
from dotenv import load_dotenv
from enum import Enum

# Discord Variables
load_dotenv()
API_TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID_INT = int(os.getenv("GUILD_ID"))
GUILD_ID = discord.Object(id=GUILD_ID_INT)

# Inventory Variables
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

# Dice Roll Variables
ROLL_COMMAND_PATTERN = r"r(?P<count>[1-9]?\d*)?d(?P<di>[1-9]\d*)(?P<modifier>(?:[\-\+][1-9]\d*)?)(?P<roll_type>(?:ad|wd)?)"
class RollType(Enum):
    Normal = 1
    Advantage = 2
    Disadvantage = 3