# dd-bot
Primarily a discord dice bot with flexible command formatting. But it's grown
to include additional functionality including custom emoji support, an 
extendable response library and a basic inventory tracking system.


## Roll Command
The roll command takes advantage of discord's auto complete fields for new
users; providing a helpful guide through the available roll parameters:
| Name     | Description                                                    |
| ---      | ---                                                            |
| count    | the number of di(ce) to roll                                   |
| di       | the number of sides on the di(ce) being rolled                 |
| modifier | the skill modifier to include when calculating the total value |
| special  | denotes cases of rolling with advantage or disadvantage        |

All of these are optional parameters, with the default values resulting in a
standard d20 roll with no modifier.

## Advanced Roll Commands
For more experienced users, dd-bot also supports imbedded roll commands. These
dice roll commands contain all the aformentioned parameters, are case
insensitive and ignore whitespace. This includes messages with multiple roll
commands located anywhere within a message.

```Shell
EXAMPLES:
roll d20        # Number of dice defaults to 1 when unspecified
ROLL d 6        # Ignores whitespaces and varied letter cases
roll d20 +4 wd  # Allows for modifiers in tandem with disadvantage
rd20            # "Roll" can be shortened to 'r' for convenience
rd20ad r2d6     # Include several roll commands in one message
r20d6           # Roll several dice together, suming the results

# Command(s) can be imbedded anywhere in messages
I to try searching the room rd20 -1
r1d10 slashing and r2d6 thunderous smite
```


## Inventory Tracking
This feature was a more recent addition to the bot, with the goal of balancing
the checkbook of large in-game currency sums (specifically glimmer). To this
end, three commands were introduced:
| Name     | Description                                      |
| ---      | ---                                              |
| add      | Increase the quantity of the specified inventory |
| subtract | Decrease the quantity of the specified inventory |
| view     | Display all the user's inventory quantities      |

These again take advantage of the autocomplete fields, making it a much more
user friendly experience.


## Response Library
There is a dictionary of canned responses to user messages found in the
```MemeReference``` class. This lookup is less flexible than the dice command
but still ignores white space, letter case and non-alphabet characters. If a
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
