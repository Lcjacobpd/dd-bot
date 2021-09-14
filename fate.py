'''
Process complex dice rolls
'''
import re
from numpy import random


class DiceRoll:
    '''Simulated dice roll'''
    def __init__(self, userName: str, message: str):
        line = message.lower()
        line = line.replace(' ', '').replace('roll', 'r')
        rolls = re.findall(r'r[0-9]*d[0-9]+[\+\-]?[0-9]*[w,d]*', line)

        # Check message for dice command,
        # return None if not present
        self.user = userName
        self.message = ''
        if len(rolls) == 0:
            return
        else:
            print('  > Let\'s roll!')

        # Else: line contains a dice command,
        # setup default parameters
        self.command = rolls[0]
        self.dice_count = 1
        self.sides = 20
        self.modifier = 0
        self.result = 0
        self.print_values = ''
        self.disadvantaged = False

        # Call decode function.
        self.decode(self.command)

        # Do not roll if invalid.
        if self.result is -1:
            return

        # Else: roll dice and display.
        self.roll()
        self.display()

    def decode(self, command: str):
        '''Get dice command details'''
        # Get dice type.
        self.sides = int(re.findall(r'd[0-9]+', command)[0][1:])

        # Check for multi-di roll.
        if command[1].isdigit():
            self.dice_count = int(re.findall(r'[0-9]+d', command)[0][:-1])
            if self.dice_count == 0:
                self.result = -1
                return  # Invalid number of dice

        # Check for modifier.
        if '+' in command or '-' in command:
            self.modifier = int(re.findall(r'[\+\-][0-9]+', command)[0])

        # Disadvantaged roll case,
        # only applicable with a single di.
        if 'wd' in command and self.dice_count == 1:
            self.disadvantaged = True

    def roll(self):
        '''Roll dice to specifications, record details'''
        # Disadvantage case,
        # keep lower of two rolls (display both).
        if self.disadvantaged is True:
            first_roll = random.randint(1, self.sides + 1)
            second_roll = random.randint(1, self.sides + 1)
            if first_roll < second_roll:
                # ' + ' is generic space to be trimmed before display.
                self.print_values = f'({first_roll} < {second_roll}) + '
                self.result = first_roll

            else:
                self.print_values = f'({second_roll} < {first_roll}) + '
                self.result = second_roll

        # Generic case,
        # roll values are cumulative (display all).
        else:
            for _ in range(1, self.dice_count + 1):
                roll = random.randint(1, self.sides + 1)
                # ' + ' separates each di in dice_count (trim last).
                self.print_values += f'{roll} + '
                self.result += roll

        # In either case, apply final modifier.
        self.result += self.modifier
        if self.modifier > 0:
            self.print_values = f'{self.print_values[:-3]} + '
            self.print_values += f'{self.modifier} + '

        elif self.modifier < 0:
            self.print_values = f'{self.print_values[:-3]} - '
            self.print_values += f'{abs(self.modifier)} - '

    def display(self):
        '''Format roll information to string, store in message'''
        # Trim excess ' + '.
        self.print_values = self.print_values[:-3]

        # Note disadvantage, if present.
        dis = ''
        if self.disadvantaged is True:
            dis = ' with disadvantage'

        # Include total if multi-di roll.
        if self.dice_count > 1 or self.modifier != 0:
            self.print_values += f' = {self.result}'

        # Format modifier to string.
        mod = ''
        if self.modifier > 0:
            mod = f'+{self.modifier}'
        elif self.modifier < 0:
            mod = f'-{abs(self.modifier)}'

        self.message = f'@{self.user}\n'
        self.message += f'> *Rolling {self.dice_count}'
        self.message += f'd{self.sides}{mod}{dis}...*\n'
        self.message += f'> {self.print_values}'
