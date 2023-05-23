import re
from numpy import random
from settings import RollType
from settings import ROLL_COMMAND_PATTERN


class dice_command:
    def __init__(self, count: int=1, di: int=20, modifier: int=0, type: RollType=RollType.Normal):
        self.count = count
        self.di = di
        self.modifier = modifier
        self.roll_type = type

    # Unecessary with new regex pattern
    # def Parse(self, rawCommand: str):
    #     match = re.match(ROLL_COMMAND_PATTERN, rawCommand)
    #     if not match: return

    #     groups = match.groupdict()
    #     self.count    = int(groups["count"])    if groups["count"]    else 1
    #     self.di       = int(groups["di"])       if groups["di"]       else 20
    #     self.modifier = int(groups["modifier"]) if groups["modifier"] else 0
    #     if groups["roll_type"] == "":   self.roll_type = RollType.Normal
    #     if groups["roll_type"] == "ad": self.roll_type = RollType.Advantage
    #     if groups["roll_type"] == "wd": self.roll_type = RollType.Disadvantage


"""
DICE ROLLER
- Determine if message contains dice command(s)
- Parse command(s) for details
- Generate psuedo random number(s)
- Return results formatted for display
"""
class dice_roller:
    response = None

    def __init__(self, message: str=""):
        self.message = message.lower().replace(r" ", "").replace("roll", "r")
        self.commands = re.findall(ROLL_COMMAND_PATTERN, self.message)
        self.Check()

    def Check(self):
        # No dice roll commands recognized, bail early
        if len(self.commands) == 0:
            return

        # Otherwise, let's roll!
        print("  > Decoding dice commands... \t" + str(self.commands))
        self.response = ""
        for parameters in self.commands:
            count    = int(parameters[0]) if parameters[0] else 1
            di       = int(parameters[1]) if parameters[1] else 20
            modifier = int(parameters[2]) if parameters[2] else 0

            roll_type = RollType.Normal
            if   str(parameters[3]) == "ad": roll_type = RollType.Advantage
            elif str(parameters[3]) == "wd": roll_type = RollType.Disadvantage

            command = dice_command(count, di, modifier, roll_type)
            self.Roll(command)

    def Roll(self, command: dice_command):
        """Simulate specified dice roll"""
        print("  > Let's roll!...")
        rollTotal = 0

        # Begin building formatted response message        
        self.response += f"> *Rolling {command.count}d{command.di}"
        self.response += "{0:+}".format(command.modifier) if command.modifier != 0     else ""
        self.response += " with advantage"    if command.roll_type == RollType.Advantage    else ""
        self.response += " with disadvantage" if command.roll_type == RollType.Disadvantage else ""
        self.response += "...*\n"

        # Roll with advantage (display both)
        if command.roll_type == RollType.Advantage:
            firstRoll  = random.randint(1, command.di + 1)
            secondRoll = random.randint(1, command.di + 1)
            if firstRoll > secondRoll:
                self.response += f"> (**{firstRoll}** > {secondRoll})"
                rollTotal = firstRoll

            else:
                self.response += f"> (**{secondRoll}** > {firstRoll})"
                rollTotal = secondRoll

        # Roll with disadvantage (display both)
        elif command.roll_type == RollType.Disadvantage:
            firstRoll  = random.randint(1, command.di + 1)
            secondRoll = random.randint(1, command.di + 1)
            if firstRoll < secondRoll:
                self.response += f"> (**{firstRoll}** < {secondRoll})"
                rollTotal = firstRoll

            else:
                self.response += f"> (**{secondRoll}** < {firstRoll})"
                rollTotal = secondRoll

        # Normal roll, values are cumulative
        else:
            self.response += "> "
            for _ in range(1, command.count + 1):
                roll = random.randint(1, command.di + 1)
                self.response += f"{roll} + "
                rollTotal += roll
            # Trim the trailing ' + ' off the end
            self.response = self.response[:-3]

        # In all cases, apply final modifier
        rollTotal += command.modifier

        # Display total value if needed
        # - Roll used several dice
        # - Roll used advantage/disadvantage
        # - Roll had a non-zero modifier
        if command.modifier == 0:
            self.response += f" = {rollTotal}" if command.count > 1 or command.roll_type != RollType.Normal else ""
        elif command.modifier > 0:
            self.response += F" + {command.modifier} = {rollTotal}"
        else:
            self.response += F" - {abs(command.modifier)} = {rollTotal}"
        self.response += "\n"
