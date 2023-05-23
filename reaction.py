import re
# import string
from enum import Enum

# TODO: Move into settings?
"""
CUSTOM DISCORD EMOJIS
- Copy the ID from discord to add your own
"""
class CustomEmoji:
    Heyo  = "<:heyo:829028736162201700>"
    Nat1  = "<:nat1:818628379967356960>"
    Nat20 = "<:nat20:818628403119783957>"

    D2Emojis = {
        "glimmer"           : "<:d2_material_glimmer:1042134639969566750>",
        "vanguard tokens"   : "<:d2_faction_vanguard:1042948486875856949>",
        "crucible tokens"   : "<:d2_faction_crucible:1042948478134923407>",
        "cryptarch tokens"  : "<:d2_faction_cryptarch:1042948479686819930>"
    }


"""
MEME REFERENCES
A canned response system for specific phrases or keywords
- Case and special character insensitive
- Easily extendable
"""
class MemeReference():
    def __init__(self, author: str, message: str):
        self.Author = author
        self.Key = re.sub("[^0-9a-z]+", "", message.lower())        
        self.Response = self.Check()

    def Check(self):
        library = {
            # Prompt            : Response
            "hellothere"        : "General Kenobi! You *are* a bold one.",
            "iamthesenate"      : "Not yet.",
            "rockandstone"      : "For Karl!",
            "whatelsedoesitdo"  : "Your mom.",
            "whatelsecanitdo"   : "Your mom.",
            "thisbotsucks"      : "No u.",
            "goodjobson"        : CustomEmoji.Heyo,
            "thatsmyboy"        : CustomEmoji.Heyo,
            "gogetemson"        : CustomEmoji.Heyo,
            "ttyl"              : "G\'night"
        }

        # No meme references recognized, bail early
        if self.Key not in library:
            return None

        print("  > Meme reference!")
        response = library[self.Key]

        # Special user case
        if response == CustomEmoji.Heyo and str(self.Author) != "Lcjacobpd#1099":
            self.Response = "You're not my dad"
        return response


# TODO: Impliment as limited user autofill command
# class Echo:
#     """
#     Puppeteer the bot's messages
#     """
#     def __init__(self) -> None:
#         self.room = ""
#         self.text = ""

#     def puppet(self, message) -> None:
#         self.room = message.split(" ")[0] 
#         self.text = " ".join(message.split(" ")[1:])

#         if not "#" in self.room:
#             self.guild = ""
#             return
#         else:
#             self.guild = self.room.split("#")[0]
#             self.room  = self.room.split("#")[1]
