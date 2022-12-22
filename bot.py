from dis import dis
import os
import typing
import discord
from dotenv import load_dotenv

from fate import DiceRoll
from reply import memeSearch
from reply import Reaction

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
    roll = DiceRoll(message.author, message.content)
    di =  roll.check()
    if di != "":
        await message.channel.send(di)

    # Check for meme reference
    meme = memeSearch(message)
    if meme is not None:
        await message.channel.send(meme)

    print ('  > Done.')

# Main body
client.run(TOKEN)