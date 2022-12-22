"""
Process dice roll commands
"""
import re
from numpy import random


class DiceRoll:
    """Wrapper for simulated dice roll"""
    def __init__(self, user: str, message: str):
        pattern = r"r[1-9]*d[1-9]{1}[\d]*[\+\-]?[1-9]*[\d]*[wad]{0,2}"

        self.user = user
        self.message = message.lower().replace(r" ", "").replace("roll", "r")
        self.cmds = re.findall(pattern, self.message)
        self.di_count = 0
        self.sides = 0
        self.mod = 0
        self.disadv = False
        self.adv = False

    def check(self) -> str:
        """Return dice results"""
        if len(self.cmds) > 0:
            return self.decode(self.cmds)
        else:
            return ""

    def decode(self, commands) -> str:
        """Get dice commands details"""
        print("  > Decoding dice commands... \t" + str(self.cmds))

        msg = ""
        for command in commands:
            # Reset between rolls
            self.mod = 0
            self.disadv = False
            self.adv = False

            self.sides = int(re.findall(r"d[1-9]{1}[0-9]*", command)[0][1:])

            # Check for multi-di roll
            dc = re.findall(r"r[1-9]*d", command)
            self.di_count = 1 if len(dc) == 1 else int(dc[0][:-1])

            # Check for modifier
            if "+" in command or "-" in command:
                m = re.findall(r"[\+\-][1-9]*[0-9]*", command)
                self.mod = int(m[0]) if len(m) > 0 else 0

            # Roll with disadvantage
            if "wd" in command and self.di_count == 1:
                self.disadv = True

            # Roll with advantage
            elif "ad" in command and self.di_count == 1:
                self.adv = True

            # Roll
            msg += "\n" + self.roll_dice()
        return msg

    def roll_dice(self) -> str:
        """Simulate specified dice roll"""
        print("  > Let's roll!...")
        result = 0
        
        msg = f"@{self.user}\n"
        msg += f"> *Rolling {self.di_count}"
        msg += f"d{self.sides}"
        msg += f"{'+' if self.mod > 0 else ''}{self.mod}" if self.mod != 0 else ""
        msg += " with disadvantage" if self.disadv else ""
        msg += " with advantage" if self.adv else ""
        msg += "...*\n"

        # Roll with disadvantage (display both)
        if self.disadv:
            r_one = random.randint(1, self.sides + 1)
            r_two = random.randint(1, self.sides + 1)
            if r_one < r_two:
                msg += f"> (**{r_one}** < {r_two})"
                result = r_one

            else:
                msg += f"> (**{r_two}** < {r_one})"
                result = r_two

        # Roll with advantage (display both)
        elif self.adv:
            r_one = random.randint(1, self.sides + 1)
            r_two = random.randint(1, self.sides + 1)
            if r_one > r_two:
                msg += f"> (**{r_one}** > {r_two})"
                result = r_one

            else:
                msg += f"> (**{r_two}** > {r_one})"
                result = r_two

        # Generic case, roll values are cumulative
        else:
            msg += "> "
            for _ in range(1, self.di_count + 1):
                roll = random.randint(1, self.sides + 1)
                msg += f"{roll} + "
                result += roll

            msg = msg[:-3]

        # In either case, apply final modifier
        result += self.mod
        if self.mod == 0:
            msg += f" = {result}" if self.di_count > 1 else ""
            return msg
        elif self.mod > 0:
            msg += f" + {self.mod} = {result}"
        else:
            msg += f" - {abs(self.mod)} = {result}"

        return msg


# r = DiceRoll("jake", "Grenade: rd8+1 Attack:rd20+4wd")
# print(r.check())
