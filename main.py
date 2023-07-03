import json
import settings
import typing
import discord
from discord.ext import commands
from discord import app_commands
from tracking import item_handler
from tracking import mote_handler
from tracking import InventoryAction
from tracking import MoteAction
from fate import dice_roller
from fate import dice_command
from settings import RollType
from reaction import MemeReference
from settings import D2_INFO


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

    #region D2Information

    async def info_autocompletion(
        interaction: discord.Interaction,
        current: str
    ) -> typing.List[app_commands.Choice[str]]:
        data = []

        # Navigate through json nodes to current keys
        options = interaction.data["options"]
        node = D2_INFO
        for option in options:
            step = option["value"]            
            if step in node.keys():
                node = node[step]

        choices = node.keys()
        for choice in choices:
            if current.lower() in choice.lower():
                data.append(app_commands.Choice(name=choice, value=choice))
        return data 

    @bot.tree.command(name="d2_information")
    @app_commands.autocomplete(category=info_autocompletion, subcategory=info_autocompletion)
    async def info(interaction: discord.Interaction, category:str, subcategory:str):
        '''Find information on a D2 topic'''
        result = D2_INFO[category][subcategory]

        f = discord.File(F"img/{result.icon}")
        embed = discord.Embed(
            colour=result.color,
            title=result.title,
            description=result.description,
        )
        
        embed.set_thumbnail(url=F"attachment://{result.icon}")                
        embed.add_field(name="Cost", value=result.cost)
        embed.insert_field_at(1, name="Days Required", value=result.days_required)
        embed.insert_field_at(2, name="Reward", value=result.reward)
        
        await interaction.response.send_message(file=f, embed=embed)

    #endregion

    #region D2Motes

    async def mote_autocompletion(
        interaction: discord.Interaction,
        current: str
    ) -> typing.List[app_commands.Choice[str]]:
        data = [ ]
        file = open(settings.MOTES_FILE)
        moteData = json.load(file)
        for key in moteData.keys():
            choice = str(key)
            if current.lower() in choice.lower():
                data.append(app_commands.Choice(name=choice, value=choice))
        return data         

    @bot.tree.command(name="mote-collect")
    @app_commands.autocomplete(owner=mote_autocompletion)
    async def collectMote(interaction: discord.Interaction, owner: str, quantity: int):
        '''Add mote(s) to a player inventory'''
        await interaction.response.send_message(mote_handler(MoteAction.Collect, owner, quantity).response)

    @bot.tree.command(name="mote-deposit")
    @app_commands.autocomplete(owner=mote_autocompletion)
    async def depositMote(interaction: discord.Interaction, owner: str):
        '''Deposite all motes from a player inventory'''
        await interaction.response.send_message(mote_handler(MoteAction.Deposit, owner).response)

    @bot.tree.command(name="mote-reset")
    async def resetMote(interaction: discord.Interaction):
        '''Reset Mote tally'''
        await interaction.response.send_message(mote_handler(MoteAction.Reset).response)

    #endregion

    @bot.command()
    @commands.is_owner()
    async def echo(ctx, *message):
        '''Echo owner's message'''
        await ctx.message.delete()
        await ctx.send(" ".join(message))

    @bot.event
    async def on_message(message):
        if message.author == bot.user:
            return  # Don't reply to yourself

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
        
        # Check for any other command if none of these
        await bot.process_commands(message)

    bot.run(settings.API_TOKEN)


if __name__ == "__main__":
    run()
