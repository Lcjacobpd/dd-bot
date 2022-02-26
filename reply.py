import re
import string

from discord import channel


class Reaction:
    # Custom Discord emojis
    heyo  = '<:heyo:829028736162201700>'
    nat1  = '<:nat1:818628379967356960>'
    nat20 = '<:nat20:818628403119783957>'


def memeSearch(message):
    '''
    Check message for meme reference, compare to dictionary and return
    '''
    key = re.sub('[^0-9a-zA-Z]+', '', message.content.lower())

    library = {
        'hellothere': 'General Kenobi! You *are* a bold one.',
        'whatelsedoesitdo': 'Your mom.',
        'whatelsecanitdo': 'Your mom.',
        'rockandstone': 'For Karl!',
        'thisbotsucks': 'No u.',
        'goodjobson': Reaction.heyo,
        'thatsmyboy': Reaction.heyo,
        'ttyl': 'G\'night'
    }

    if key in library:
        print('  > Meme reference!')
        meme = library[key]

        # Special user case.
        if meme == Reaction.heyo and str(message.author) != 'Lcjacobpd#1099':
            meme = 'You ain\'t my dad.'

        return meme
    
    else:
        return None


class Echo:
    '''
    Puppeteer the bot's messages
    '''
    def __init__(self) -> None:
        self.room = ''
        self.text = ''

    def puppet(self, message) -> None:
        self.room = message.split(' ')[0] 
        self.text = ' '.join(message.split(' ')[1:])

        if not "#" in self.room:
            self.guild = ""
            return
        else:
            self.guild = self.room.split("#")[0]
            self.room  = self.room.split("#")[1]
