# dd-bot

A discord dice bot with flexible command formatting, normal distribution
random number generation and an extendable response library.

<br/>

## Command Formatting

All of the following are examples of valid command formats:
```bash
roll d20     # Number of dice defaults to 1
roll d 6     # Ignores whitespace
roll d20 -4  # Allows for modifiers
rd20         # "Roll" shorthands to 'r'
r d20 +2 wd  # Roll with mod and disadvantage

# Commands can be imbedded in messages
I search the room rd20 -1
roll d20 +3 I flatter the barmaid.
```

<br/>

## Response Library

There is a dictionary of canned responses to user methods found in the
memeSearch() function. This method also ignores white space, case and non
alphabet characters. If a user message can be used as a dictionary key,
the method will return the response. 
```Python
library = {
    'hellothere': 'General Kenobi!',
    'iamthesenete': 'Not yet.',
    'whatelsedoesitdo': 'Your mom.',
    'whatelsecanitdo': 'Your mom.',
    'rockandstone': 'For Karl!'
}
```

<br/>

-------------------------------------------------------------------------------