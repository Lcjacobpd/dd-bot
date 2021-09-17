"""
Process dice roll commands
"""
import re
from numpy import random


class DiceRoll:
    """Wrapper for simulated dice roll"""
    def __init__(self, user: str, message: str):
        pattern = r"r[0-9]*d[0-9]+[\+\-]?[0-9]*[w,d]*"

        self.user = user
        self.message = message.lower().replace(" ", "").replace("roll", "r")
        self.cmds = re.findall(pattern, self.message)
        self.di_count = 0
        self.sides = 0
        self.mod = 0
        self.disadv = False

    def check(self) -> str:
        """Return dice results"""
        if len(self.cmds) > 0:
            return self.decode(self.cmds[0])
        else:
            return ""

    def decode(self, command: str) -> str:
        """Get dice command details"""
        print("  > Decoding dice command...")
        self.sides = int(re.findall(r"d[0-9]+", command)[0][1:])

        # Check for valid/multi-di roll.
        self.di_count = re.findall(r"[0-9]+d", command)
        self.di_count = 1 if len(self.di_count) == 0 else int(self.di_count[0][:-1])
        if self.di_count == 0:
            return ""  # Invalid number of dice.

        # Check for modifier.
        if "+" in command or "-" in command:
            self.mod = int(re.findall(r"[\+\-][0-9]+", command)[0])

        # Disadvantaged roll case (single di only).
        if "wd" in command and self.di_count == 1:
            self.disadv = True

        return self.roll_dice()

    def roll_dice(self) -> str:
        """Simulate specified dice roll"""
        print("  > Let's roll!...")
        result = 0
        
        msg = f"@{self.user}\n"
        msg += f"> *Rolling {self.di_count}"
        msg += f"d{self.sides}"
        msg += f"{self.mod}" if self.mod != 0 else ""
        msg += " with disadvantage" if self.disadv else ""
        msg += "...*\n"

        # Disadvantage case (display both).
        if self.disadv:
            r_one = random.randint(1, self.sides + 1)
            r_two = random.randint(1, self.sides + 1)
            if r_one < r_two:
                msg += f"> ({r_one} < {r_two})"
                result = r_one

            else:
                msg += f"> ({r_two} < {r_one})"
                result = r_two

        # Generic case, roll values are cumulative.
        else:
            msg += "> "
            for _ in range(1, self.di_count + 1):
                roll = random.randint(1, self.sides + 1)
                msg += f"{roll} + "
                result += roll

            msg = msg[:-3]

        # In either case, apply final modifier.
        result += self.mod
        if self.mod == 0:
            msg += f" = {result}" if self.di_count > 1 else ""
            return msg
        elif self.mod > 0:
            msg += f" + {self.mod} = {result}"
        else:
            msg += f" - {abs(self.mod)} = {result}"

        return msg


# r = DiceRoll("jake", "r d6")
# print(r.check())
