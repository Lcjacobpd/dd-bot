# dd-bot

Primarily a discord dice bot with flexible command formatting and normal
distribution random number generation. But it's grown to include
additional functionality including an extendable response library.

<br/>

## Command Formatting

All of the following are examples of valid command formats:
```
roll d20     # Number of dice defaults to 1
roLl d 6     # Ignores whitespace and letter case
roll d20 -4  # Allows for modifiers
rd20         # "Roll" shorthands to 'r'
r d20 +2 wd  # Roll with both modifer and disadvantage (or advantage)
rd20ad r2d6  # Include several roll commands in one message

# Commands can be imbedded anywhere in messages
I search the room rd20 -1
roll d20 +3 Can I flatter the barmaid?
```

<br/>

## Response Library

There is a dictionary of canned responses to user messages found in the
```memeSearch()``` function. This method also ignores white space, letter
case and non alphabet characters. If a user message can be used as a
dictionary key, the method will return the response. 
```Python
library = {
    # prompt : response
    'hellothere': 'General Kenobi!',
    'iamthesenete': 'Not yet.',
    'rockandstone': 'For Karl!'
}
```
