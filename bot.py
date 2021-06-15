import os
import discord
from dotenv import load_dotenv

from fate import DiceRoll
from reply import Reaction
from reply import Echo
from reply import memeSearch


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
client = discord.Client()

'''
Listeners
'''
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
            await message.add_reaction(Reaction.nat1) 

        # React if it was a bad dice roll
        if 'Rolling 1d20...' in message.content and message.content.endswith('> 20'):
            await message.add_reaction(Reaction.nat20)

        return

    print('Processing new message...')

    # Check for dice roll
    fate = DiceRoll(message.author, message.content)
    if fate.message != '':
        await message.channel.send(fate.message)

    # Check for meme reference
    meme = memeSearch(message)
    if meme is not None:
        await message.channel.send(meme)

    # Check for puppet
    if message.channel == discord.utils.get(message.guild.text_channels, name='echo'):
        echo = Echo()
        echo.puppet(message.content)
        channel = discord.utils.get(message.guild.text_channels, name=echo.room)
        if channel != None:
            print(' > Echoing!')
            await channel.send(echo.text)
        else:
            pass

    print ('  > Done.')

# Main body
client.run(TOKEN)