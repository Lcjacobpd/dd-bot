# dd-bot

Primarily a discord dice bot with flexible command formatting. But it's grown
to include additional functionality including custom emoji support, an 
extendable response library and a basic inventory tracking system.


## Command Formatting
Dice roll commands contain several optional parameters, are case insensitive,
ignore whitespace allow for rolls to be performed with modifiers and/or with
advantage/disadvantage. Additionally, several commands can be imbedded
anywhere within a message.

```
EXAMPLES:
roll d20        # Number of dice defaults to 1 when unspecified
ROLL d 6        # Ignores whitespaces and varied letter cases
roll d20 +4 wd  # Allows for modifiers in tandem with disadvantage
rd20            # "Roll" can be shortened to 'r' for convenience
rd20ad r2d6     # Include several roll commands in one message
r20d6           # Roll several dice together, suming the results

# Command(s) can be imbedded anywhere in messages
I'm going to try searching the room rd20 -1
r1d10 slashing and r2d6 for thunderous smite
```


## Response Library
There is a dictionary of canned responses to user messages found in the
```MemeReference``` class. This lookup is less flexible than the dice command
but it also ignores white space, letter case and non-alphabet characters. If a
user's message can be found as a dictionary key, the method will return the
response.

```Python
library = {
    # Prompt            : Response
    "hellothere"        : "General Kenobi! You *are* a bold one.",
    "iamthesenate"      : "Not yet.",
    "rockandstone"      : "For Karl!",
    ...
}
```

<br/>

## Inventory Tracking
The `InventoryHandler` class is the most recent addition to the bot, with the 
goal of managing the tally of large in-game currency sums (specifically 
glimmer). Adding three commands to list, add and subtract from your tracked
inventory items respectively. With optional support for custom emojis if one
is linked to the item being tracked.

```
EXAMPLES:
#loot                    - Display all recorded inventory
#add <quantity> <item>   - Add amount to inventory item
#sub <quantity> <item>   - Subtract amount from inventory item
```