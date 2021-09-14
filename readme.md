# dd-bot

Primarily a discord dice bot with flexible command formatting and normal
distribution random number generation. But it's grown to include quite a
bit of additional functionality including an extendable response library,
tic-tac-toe games between two users and collecting daily reset news for
Destiny 2.

<br/>

## Command Formatting

All of the following are examples of valid command formats:
```bash
roll d20     # Number of dice defaults to 1
roLl d 6     # Ignores whitespace and letter case
roll d20 -4  # Allows for modifiers
rd20         # "Roll" shorthands to 'r'
r d20 +2 wd  # Can roll with both modifer and disadvantage

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

<br/>

## Tic-Tac-Toe

This was a fun little piece to impliment. Simply start a message with "ttt"
followed by an @mention to another user to start a game. At the moment dd-bot
isn't smart enough to play you herself, perhaps sometime down the road.

<br/>

## Destiny 2 News

Information reguarding Destiny 2's daily reset can be tracked and displayed;
vendor sales and legend/master lost sectors in particular. Specific users, or
guardians as I will refer to them for the remainder of this explanation, can
bookmark items of interest to be mentioned in the bot's response upon the
news being displayed. 

For example, if a guardian is interested in "charged with light" mods from
Ada: ```remind me: charged with light```. More bookmarks can be added in
subsequent messages or chained together: ```remind me: warmind, E15```.
Should the daily news contain any of these key words/phrases, the guardian in
question will receive an @mention.