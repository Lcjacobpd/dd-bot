import settings
import typing
import discord
from discord.ext import commands
from discord import app_commands
from tracking import item_handler
from tracking import InventoryAction
from fate import dice_roller
from fate import dice_command
from settings import RollType
from reaction import MemeReference

def run():
    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix='/', intents=intents)

    @bot.event
    async def on_ready():
        bot.tree.copy_global_to(guild=settings.GUILD_ID)
        await bot.tree.sync(guild=settings.GUILD_ID)

        print(F"{bot.user} has connected to Discord!")

    #region InventoryCommands

    async def inv_autocompletion(
        interaction: discord.Interaction,
        current: str
    ) -> typing.List[app_commands.Choice[str]]:
        data = []
        for choice in settings.TRACKED_ITEMS:
            if current.lower() in choice.lower():
                data.append(app_commands.Choice(name=choice, value=choice))
        return data 

    @bot.tree.command(name="inventory-add")
    @app_commands.autocomplete(item=inv_autocompletion)    
    async def add(interaction: discord.Interaction, quantity: int, item: str):
        '''Add item(s) to inventory'''
        await interaction.response.send_message(item_handler(interaction.user, InventoryAction.Add, quantity, item).response)

    @bot.tree.command(name="inventory-subtract")
    @app_commands.autocomplete(item=inv_autocompletion)
    async def subtract(interaction: discord.Interaction, quantity: int, item: str):
        '''Subtract item(s) from inventory'''
        await interaction.response.send_message(item_handler(interaction.user, InventoryAction.Subtract, quantity, item).response)

    @bot.tree.command(name="inventory-view")
    async def total(interaction: discord.Interaction):
        '''Display inventory totals'''
        await interaction.response.send_message(item_handler(interaction.user, InventoryAction.Total).response)

    #endregion

    #region DiceCommands

    async def roll_autocompletion(
        interaction: discord.Interaction,
        current: str
    ) -> typing.List[app_commands.Choice[str]]:
        data = []
        for choice in [ "advantage", "disadvantage" ]:
            if current.lower() in choice.lower():
                data.append(app_commands.Choice(name=choice, value=choice))
        return data 

    @bot.tree.command()
    @app_commands.autocomplete(special=roll_autocompletion)
    async def roll(interaction: discord.Interaction, count:int=1, di:int=20, modifier:int=0, special: str=""):
        '''Make a dice roll'''
        roll_type = RollType.Normal if special == "" else RollType.Advantage if special == "advantage" else RollType.Disadvantage
        command = dice_command(count, di, modifier, roll_type)
        roller = dice_roller()
        roller.Roll(command)
        await interaction.response.send_message(roller.response)

    #endregion

    @bot.event
    async def on_message(message):
        if message.author == bot.user:
            return  # Don't reply to yourself
        # DEBUG:
        # print(type(message))
        # print(dir(message))

        print('Processing new message...')

        # Check for complex dice roll commands(s)
        roll = dice_roller(message.content)
        if roll.response is not None:
            await message.reply(roll.response)
            return

        # Check for meme reference
        meme = MemeReference(message.author, message.content)
        if meme.response is not None:
            await message.reply(meme.response)
            return
    
    bot.run(settings.API_TOKEN)


if __name__ == "__main__":
    run()
