import re
from enum import Enum
from numpy import random


"""
GLOBAL DICE COMMAND RECOGNITION PATTERN
Base:
- The letter 'r' followed by
- An optional number > 0,
- The letter 'd' followed by
- A required number > 0
Optional:
- A number modifier preceeded by either +/-
- The letters 'ad' or 'wd' denoting special roll type
"""
PATTERN = r"r(?:[1-9]*\d)?d[1-9]\d*(?:[\+\-][1-9][\d]*)?(?:ad|wd)?"


class RollType(Enum):
    Normal = 1
    Advantage = 2
    Disadvantage = 3


class DiceCommand:
    def __init__(self, rawCommand: str):        
        diCount   = re.findall(r"r([1-9]\d*)d", rawCommand)
        sideCount = re.findall(r"d([1-9]\d*)", rawCommand)
        modifier  = re.findall(r"[/+/-][1-9]\d*", rawCommand)
        rollType  = re.findall(r"(ad|wd)", rawCommand)

        # Record parameters or assign default
        self.DiCount   = 1 if len(diCount) == 0 else int(diCount[0])
        self.SideCount = 4 if len(sideCount) == 0 else int(sideCount[0])
        self.Modifier  = 0 if len(modifier) == 0 else int(modifier[0])
        self.Type = RollType.Normal if len(rollType) == 0 or self.DiCount > 1 else RollType.Advantage if rollType[0] == "ad" else RollType.Disadvantage


"""
DICE ROLLER
- Determine if message contains dice command(s)
- Parse command(s) for details
- Generate psuedo random number(s)
- Return results formatted for display
"""
class DiceRoller:
    def __init__(self, author: str, message: str):
        self.Author = author
        self.Message = message.lower().replace(r" ", "").replace("roll", "r")
        self.Commands = re.findall(PATTERN, self.Message)

    def Check(self) -> str:
        # No dice roll commands recognized, bail early
        if len(self.Commands) == 0:
            return ""

        # Otherwise, let's roll!
        print("  > Decoding dice commands... \t" + str(self.Commands))
        response = f"@{self.Author}\n"
        for rawCommand in self.Commands:
            response += self.Roll(DiceCommand(rawCommand))

        return response

    def Roll(self, command: "DiceCommand") -> str:
        """Simulate specified dice roll"""
        print("  > Let's roll!...")
        rollTotal = 0

        # Begin building formatted response message        
        response = f"> *Rolling {command.DiCount}d{command.SideCount}"
        response += "{0:+}".format(command.Modifier) if command.Modifier != 0     else ""
        response += " with advantage"    if command.Type == RollType.Advantage    else ""
        response += " with disadvantage" if command.Type == RollType.Disadvantage else ""
        response += "...*\n"

        # Roll with advantage (display both)
        if command.Type == RollType.Advantage:
            firstRoll  = random.randint(1, command.SideCount + 1)
            secondRoll = random.randint(1, command.SideCount + 1)
            if firstRoll > secondRoll:
                response += f"> (**{firstRoll}** > {secondRoll})"
                rollTotal = firstRoll

            else:
                response += f"> (**{secondRoll}** > {firstRoll})"
                rollTotal = secondRoll

        # Roll with disadvantage (display both)
        elif command.Type == RollType.Disadvantage:
            firstRoll  = random.randint(1, command.SideCount + 1)
            secondRoll = random.randint(1, command.SideCount + 1)
            if firstRoll < secondRoll:
                response += f"> (**{firstRoll}** < {secondRoll})"
                rollTotal = firstRoll

            else:
                response += f"> (**{secondRoll}** < {firstRoll})"
                rollTotal = secondRoll

        # Normal roll, values are cumulative
        else:
            response += "> "
            for _ in range(1, command.DiCount + 1):
                roll = random.randint(1, command.SideCount + 1)
                response += f"{roll} + "
                rollTotal += roll
            # Trim the trailing ' + ' off the end
            response = response[:-3]

        # In all cases, apply final modifier
        rollTotal += command.Modifier

        # Display total value if needed
        # - Roll used several dice
        # - Roll used advantage/disadvantage
        # - Roll had a non-zero modifier
        if command.Modifier == 0:
            response += f" = {rollTotal}" if command.DiCount > 1 or command.Type != RollType.Normal else ""
        elif command.Modifier > 0:
            response += f" + {command.Modifier} = {rollTotal}"
        else:
            response += f" - {abs(command.Modifier)} = {rollTotal}"

        return response+"\n"


# DEBUG values
# r = DiceRoller("jake", "r4d4 rd20+4wd rd10ad rd8+")
# print(r.Check())