import os
import re
import discord
from numpy import random
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
client = discord.Client()

# Custom emojis
heyo = '<:heyo:829028736162201700>'
nat1 = '<:nat1:818628379967356960>'
nat20 = '<:nat20:818628403119783957>'

class DiceRoll:
    def __init__(self, userName: str, message: str):      
        line = message.lower()
        line = line.replace(' ','').replace('roll', 'r')
        rolls = re.findall(r'r[0-9]*d[0-9]+[\+\-]?[0-9]*[w,d]*', line)

        # Check message for dice command,
        # return None if not present  
        self.user = userName
        self.message = ''
        if len(rolls) == 0:
            print('Not a dice roll')
            return 

        # Else: line contains a dice command,
        # setup default parameters
        self.command = rolls[0]
        self.diceCount = 1
        self.sides = 20
        self.modifier = 0
        self.result = 0
        self.printValues = ''
        self.disadvantaged = False

        # Call decode function.
        self.decode(self.command)

        # Do not roll if invalid.
        if self.result is None:
            return

        # Else: roll dice and display.
        self.roll()
        self.display()

    def decode(self, command:str):
        '''
        Get dice command details
        '''
        # Get dice type.
        self.sides = int(re.findall(r'd[0-9]+', command)[0][1:])

        # Check for multi-di roll.
        if command[1].isdigit():
            self.diceCount = int(re.findall(r'[0-9]+d', command)[0][:-1])
            if self.diceCount == 0:
                self.result = None
                return  # Invalid number of dice

        # Check for modifier.
        if '+' in command or '-' in command:
            self.modifier = int(re.findall(r'[\+\-][0-9]+', command)[0])

        # Disadvantaged roll case,
        # only applicable with a single di.
        if 'wd' in command and self.diceCount == 1:
            self.disadvantaged = True

    def roll(self):
        '''
        Roll dice to specifications, record details
        '''
        # Disadvantage case,
        # keep lower of two rolls (display both).
        if self.disadvantaged is True:
            firstRoll = random.randint(1, self.sides + 1)
            secondRoll = random.randint(1, self.sides + 1)
            if firstRoll < secondRoll:
                # ' + ' is generic space to be trimmed before display.
                self.printValues = f'({firstRoll} < {secondRoll}) + '
                self.result = firstRoll

            else:
                self.printValues = f'({secondRoll} < {firstRoll}) + '
                self.result = secondRoll
        
        # Generic case,
        # roll values are cumulative (display all).
        else:
            for _ in range(1, self.diceCount + 1):
                roll = random.randint(1, self.sides + 1)
                # ' + ' separates each di in diceCount (trim last).
                self.printValues += f'{roll} + '
                self.result += roll

        # In either case, apply final modifier.
        self.result += self.modifier
        if self.modifier > 0:
            self.printValues = f'{self.printValues[:-3]} + {self.modifier} + '
        elif self.modifier < 0:
            self.printValues = f'{self.printValues[:-3]} - {abs(self.modifier)} - '
        
    def display(self):
        '''
        Format roll information to string, store in message
        '''
        # Trim excess ' + '.
        self.printValues = self.printValues[:-3]
        
        # Note disadvantage, if present.
        dis = ''
        if self.disadvantaged is True:
            dis = ' with disadvantage'

        # Include total if multi-di roll.
        if self.diceCount > 1 or self.modifier != 0:
            self.printValues += f' = {self.result}'

        # Format modifier to string.
        mod=''
        if self.modifier > 0:
            mod = f'+{self.modifier}'
        elif self.modifier < 0:
            mod = f'-{abs(self.modifier)}'

        self.message = f'@{self.user}\n'
        self.message += f'> *Rolling {self.diceCount}d{self.sides}{mod}{dis}...*\n'
        self.message += f'> {self.printValues}'


def memeSearch(message):
    '''
    Check message for meme reference,
    compare to dictionary and return
    '''
    key = re.sub('[^0-9a-zA-Z]+', '', message.content.lower())

    library = {
        'hellothere': 'General Kenobi!',
        'iamthesenete': 'Not yet.',
        'whatelsedoesitdo': 'Your mom.',
        'whatelsecanitdo': 'Your mom.',
        'rockandstone': 'For Karl!',
        'thisbotsucks': 'No u.',
        'dumbbot': 'No u.',
        'goodjobson': heyo,
        'fuckyou': 'No u.',
        'thatsmyboy': heyo
    }

    if key in library:
        print('Meme reference')
        meme = library[key]

        # Special user case.
        if meme == heyo and str(message.author) != 'Lcjacobpd#1099':
            meme = 'You ain\'t my dad.'

        return meme
    
    else:
        return None


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    # Don't reply to yourself
    if message.author == client.user:

        # React if it was a bad dice roll
        if 'Rolling 1d20...' in message.content and message.content.endswith('> 1'):
            await message.add_reaction('🇫')
            await message.add_reaction(nat1) 

        # React if it was a bad dice roll
        if 'Rolling 1d20...' in message.content and message.content.endswith('> 20'):
            await message.add_reaction(nat20)
        return

    # Check for dice roll
    fate = DiceRoll(message.author, message.content)
    if fate.message != '':
        await message.channel.send(fate.message)

    # Check for meme reference
    meme = memeSearch(message)
    if meme is not None:
        await message.channel.send(meme)


# Main body
client.run(TOKEN)