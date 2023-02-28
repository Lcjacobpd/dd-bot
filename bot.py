from dis import dis
import os
import typing
import discord
from dotenv import load_dotenv

from fate import DiceRoller
from inventory import InventoryHandler
from reaction import MemeReference
from reaction import CustomEmoji

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
            await message.add_reaction(CustomEmoji.Nat1) 

        # React if it was a good dice roll
        if 'Rolling 1d20...' in message.content and message.content.endswith('> 20'):
            await message.add_reaction(CustomEmoji.Nat20)

        return

    print('Processing new message...')

    # Check for dice roll
    roll = DiceRoller(message.author, message.content)
    if roll.Response is not None:
        await message.channel.send(roll.Response)

    # Check for meme reference
    meme = MemeReference(message.author, message.content)
    if meme.Response is not None:
        await message.channel.send(meme.Response)

    # Check for inventory request
    inventory = InventoryHandler(message.author, message.content)
    if inventory.Response is not None:
        await message.channel.send(inventory.Response)

    print ('  > Done.')

# Main body
client.run(TOKEN)