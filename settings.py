import os
import discord
from dotenv import load_dotenv
from enum import Enum


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

    #d2_emojis
    d2_cabal     = "<:2d_faction_cabal:1042948476297814100>"
    d2_crucible  = "<:d2_faction_crucible:1042948478134923407>"
    d2_cryptarch = "<:d2_faction_cryptarch:1042948479686819930>"
    d2_drifter   = "<:d2_faction_gunsmith:1042948481247084545>"
    d2_fallen    = "<:d2_faction_fallen:1042948482631225414>"
    d2_glimmer   = "<:d2_material_glimmer:1042134639969566750>"
    d2_gunsmith  = "<:d2_faction_gunsmith:1042948484166336542>"
    d2_hive      = "<:d2_faction_hive:1042948485630132324>"
    d2_mote      = "<:d2_material_mote:1123820535533535313>"
    d2_tech      = "<:d2_faction_tech:1068273471928406087>"
    d2_vanguard  = "<:d2_faction_vanguard:1042948486875856949>"
    d2_vex       = "<:d2_faction_vex:1042948488733921341>"

    #2d_emoji mappings
    d2_emojis = {
        "glimmer"           : d2_glimmer,
        "gambit tokens"     : d2_drifter,
        "crucible tokens"   : d2_crucible,
        "cryptarch tokens"  : d2_cryptarch,
        "vanguard tokens"   : d2_vanguard
    }

#endregion

#region Inventory Variables

DATA_FILE = "data.json"
TRACKED_ITEMS = [
    "glimmer",
    "gambit tokens",
    "crucible tokens",
    "cryptarch tokens",
    "vanguard tokens"
]
class InventoryAction(Enum):
    Add = 1
    Subtract = 2
    Total = 3

MOTES_FILE = "motes.json"
class MoteAction(Enum):
    Collect = 1
    Deposit = 2
    Reset = 3

#endregion

#region Dice Roll Variables

ROLL_COMMAND_PATTERN = r"r(?P<count>[1-9]?\d*)?d(?P<di>[1-9]\d*)(?P<modifier>(?:[\-\+][1-9]\d*)?)(?P<roll_type>(?:ad|wd)?)"
class RollType(Enum):
    Normal = 1
    Advantage = 2
    Disadvantage = 3

#endregion

class InfoCard:
    def __init__(self, title: str, icon: str, color: discord.Colour, cost: str, days_required: str, description: str, reward: str):
        self.title = title
        self.icon = icon
        self.color = color
        self.cost = cost
        self.days_required = days_required
        self.description = description
        self.reward = reward


D2_INFO = {
    "Downtime" : {
        "Artifact": InfoCard(
            title="Study an Artifact",
            icon="d2_faction_cryptarch.png",
            color=discord.Colour.from_str("#d68a13"),
            cost=None,
            days_required="1",
            description="*Determine the use or the abilities of an Exotic or other artifact. Requires an Arcana or Investigation roll depending on the item. On failure the item remains unknown.*\n\n*During this time you can also choose to attune to the item.*",
            reward=F"{CustomEmoji.d2_cryptarch} XP on success"
        ),
        "Crucible": InfoCard(
            title="Enter the Crucible",
            icon="d2_faction_crucible.png",
            color=discord.Colour.from_str("#d64119"),
            cost=None,
            days_required="2",
            description="*Choose Matchmaking, or a specific gamemode. Easier gamemodes have increased chance of winning, but lower rewards.*\n\n*The inverse is true for higher difficulty gamemodes.*",
            reward=F"{CustomEmoji.d2_glimmer}, {CustomEmoji.d2_crucible} XP and {CustomEmoji.d2_crucible} tokens"
        ),
        "Cryptarchy": InfoCard(
            title="Learn Skill at Cryptarchy",
            icon="d2_faction_cryptarch.png",
            color=discord.Colour.from_str("#d68a13"),
            cost=F"1,000 {CustomEmoji.d2_glimmer}",
            days_required="1-7",
            description="*Requires a roll based on the days spent studying. 1½ levels of Proficiency on success and ½ level on failure.*\n\n*Requires a total of 12 levels of Proficiency to graduate.*",
            reward=F"{CustomEmoji.d2_cryptarch} XP for each day"
        ),
        "Decrypt": InfoCard(
            title="Decrypt an Engram",
            icon="d2_faction_cryptarch.png",
            color=discord.Colour.from_str("#d68a13"),
            cost=F"1000 {CustomEmoji.d2_glimmer}",
            days_required="1",
            description="*Engram decryption is free if done yourself, but risks the chance of failure; producing only glimmer.*\n\n*Max of 2 engrams per day, unless done by the Cryptarchy.*",
            reward=F"{CustomEmoji.d2_cryptarch} XP*\n\n*additional if done yourself"
        ),
        "Equipment": InfoCard(
            title="Craft or Repair Equipment",
            icon="d2_faction_tech.png",
            color=discord.Colour.from_str("#6e7f86"),
            cost=F"⅓ equipment cost {CustomEmoji.d2_glimmer}\n1,000 {CustomEmoji.d2_glimmer}",
            days_required="Varied",
            description="*Crafting or repairs only costs ⅓ the listed equipment's glimmer cost if done yourself but requires the proper tools and risks the chance of failure. Success awards XP for either the Tech faction or the Gunsmith depending on the context.*\n\n*Alternatively, success can be guaranteed for an additional price with the corresponding faction.*",
            reward=F"{CustomEmoji.d2_tech} or {CustomEmoji.d2_gunsmith} XP"
        ),
        "Gambit": InfoCard(
            title="Drifter's Gambit",
            icon="d2_faction_drifter.png",
            color=discord.Colour.from_str("#1c6b54"),
            cost=None,
            days_required="3",
            description="*Play the Drifter's game of high risk/high reward against other guardians, clear waves of enemies and bank motes of darkness into Drifter's cache to summon a massive Taken combatant called the Primeval. The Primeval has a high chance of dropping legendary engrams.*\n\n*The game is not sanctioned by the Vanguard; there is serious risk to life and limb*",
            reward=F"Legendary Engrams, {CustomEmoji.d2_glimmer}, and {CustomEmoji.d2_drifter} XP"
        ),
        "Patrol": InfoCard(
            title="Patrol the Wilds",
            icon="d2_faction_vanguard.png",
            color=discord.Colour.from_str("#7250cd"),
            cost=None,
            days_required="2",
            description="*Choose a destination to patrol. Specified planetary destinations will yield different materials. Can optionally be done in service to the Vanguard or the Drifter.*\n\n*Patrols done in service reward faction XP at the cost of half of the glimmer collected.*",
            reward=F"{CustomEmoji.d2_glimmer} with optional\n{CustomEmoji.d2_vanguard} or {CustomEmoji.d2_drifter} XP"
        ),
        "Range": InfoCard(
            title="Shooting Range Practice",
            icon="d2_faction_gunsmith.png",
            color=discord.Colour.from_str("#456cb8"),
            cost=F"100 {CustomEmoji.d2_glimmer} for Simple\n 250 {CustomEmoji.d2_glimmer} for Martial",
            days_required="1-7",
            description="*Gain Proficiency with a weapon, or improve the Critical Hit Range for a time. Each day spent at the range increases the chance for success at Proficiency, or lengthens the effect of the Critical Hit Range increase.*\n\n*Requires 6 levels to be proficient with a new weapon, 12 to be proficient with the weapon type. 1½ levels gained on success, ½ a level gained on failure.*",
            reward=F"{CustomEmoji.d2_gunsmith} XP for each day"
        ),
        "Tower": InfoCard(
            title="Tower Activities",
            icon="d2_faction_vanguard.png",
            color=discord.Colour.from_str("#7250cd"),
            cost=None,
            days_required="3",
            description="*Working in the tower encompasses various activies and provides a variety of rewards depending on the subject matter(s) and faction(s) involved.*",
            reward=F"{CustomEmoji.d2_glimmer} and/or Faction Tokens"
        ),
    },
    "Token" : {
        "Crucible" : InfoCard(
            title="Crucible Token",
            icon="d2_faction_crucible.png",
            color=discord.Colour.from_str("#d64119"),
            description="*Can be used before any attack roll. When used, the next roll is automatically a critical hit if the attack lands successfully. If the attack misses the token is consumed with no effect.*",
            cost=None,
            days_required=None,
            reward=None
        ),
        "Cryptarch" : InfoCard(
            title="Cryptarch Token",
            icon="d2_faction_cryptarch.png",
            color=discord.Colour.from_str("#d68a13"),
            description="*Can be redeemed for a free engram decryption. An additional token can be be redeemed to focus an engram, giving you more agency over the outcome of the engram.*",
            cost=None,
            days_required=None,
            reward=None
        ),
        "Gambit" : InfoCard(
            title="Gambit Token",
            icon="d2_faction_drifter.png",
            color=discord.Colour.from_str("#1c6b54"),
            description="*Flip a gambit token to summon a random enemy to your side, this enemy will act as your minion until it dies and is returned to wherever Drifter plucked it from.*",
            cost=None,
            days_required=None,
            reward=None
        ),
        "Vanguard" : InfoCard(
            title="Vanguard Token",
            icon="d2_faction_vanguard.png",
            color=discord.Colour.from_str("#7250cd"),
            description="*Can be consumed to reroll any roll. This includes both the rolls of party members and the rolls of enemy combatants. These rolls can only be rerolled once.*",
            cost=None,
            days_required=None,
            reward=None
        ),
    }
}