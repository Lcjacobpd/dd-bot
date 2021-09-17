import os
import typing
import discord
from dotenv import load_dotenv

from fate import DiceRoll
from games import TicTacToe
from reply import Reaction
from reply import Echo
from reply import memeSearch

from destiny2 import Destiny
from destiny2 import new_reminder


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
client = discord.Client()

'''
Global
'''
ttt = TicTacToe()

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

    # Check for Destiny2 request
    d2 = Destiny(message.author, message.content)
    if d2.check() != "":
        await message.channel.send(d2)

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

    if message.content.startswith('ttt'):
        ttt.build(message)
        await message.channel.send(ttt.display())

    print ('  > Done.')

@client.event
async def on_reaction_add(reaction, user):
    message = reaction.message
    atee = message.content.split('\n')[0][3:-1]

    if str(message.author) == 'Fate#8091' and str(user.id) == atee:
        await message.clear_reactions()
        update = ttt.edit(reaction)
        if update != None:
            await message.edit(content=update)

# Main body
client.run(TOKEN)