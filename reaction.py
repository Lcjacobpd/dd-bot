import re
from settings import CustomEmoji
from settings import PARENT_ID


"""
MEME REFERENCES
A canned response system for specific phrases or keywords
- Case and special character insensitive
- Easily extendable
"""
class MemeReference():
    response = None

    def __init__(self, author: str, message: str):
        self.author = str(author)
        self.key = re.sub("[^0-9a-z]+", "", str(message).lower())        
        self.Check()

    def Check(self):
        library = {
            # Prompt            : Response
            "hellothere"        : "General Kenobi! You *are* a bold one.",
            "iamthesenate"      : "Not yet.",
            "rockandstone"      : "For Karl!",
            "whatelsedoesitdo"  : "Your mom.",
            "whatelsecanitdo"   : "Your mom.",
            "thisbotsucks"      : "No u.",
            "goodjobson"        : CustomEmoji.heyo,
            "thatsmyboy"        : CustomEmoji.heyo,
            "gogetemson"        : CustomEmoji.heyo,
            "ttyl"              : "G\'night"
        }

        # No meme references recognized, bail early
        if self.key not in library:
            return

        print("  > Meme reference!")
        self.response = library[self.key]

        # Special user case
        if self.response == CustomEmoji.heyo and str(self.author) != PARENT_ID:
            self.response = "You're not my dad"
        return self.response
