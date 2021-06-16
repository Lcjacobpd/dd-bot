import re

class TicTacToe:
    blank = ':white_square_button:'
    red   = ':o2:'
    blue  = ':regional_indicator_x:'

    def __init__(self):
        pass

    def build(self, message):
        print('  > Tic Tac Toe: Go!')

        self.p1 = f'<@!{message.author.id}>'
        self.p2 = re.findall(r'<@![0-9]+>', message.content)[0]
        self.players = [self.p1, self.p2]
        self.active = 0

        self.board = [
            0, 0, 0,
            0, 0, 0,
            0, 0, 0
        ]

    def display(self):
        msg = ''
        for pos, sqr in enumerate(self.board):
            if sqr == 0: msg += TicTacToe.blank
            elif sqr == 1: msg += TicTacToe.red
            elif sqr == 2: msg += TicTacToe.blue

            if pos == 2 or pos == 5:
                msg += '\n'

        # Check winstates
        if (self.board[0] > 0 and self.board[0] == self.board[1] == self.board[2] or
            self.board[3] > 0 and self.board[3] == self.board[4] == self.board[5] or
            self.board[6] > 0 and self.board[6] == self.board[7] == self.board[8] or
            
            self.board[0] > 0 and self.board[0] == self.board[3] == self.board[6] or
            self.board[1] > 0 and self.board[1] == self.board[4] == self.board[7] or
            self.board[2] > 0 and self.board[2] == self.board[5] == self.board[8] or
            
            self.board[0] > 0 and self.board[0] == self.board[4] == self.board[8] or
            self.board[6] > 0 and self.board[6] == self.board[4] == self.board[2]):
            
            # Toggle active player
            if self.active == 1: self.active = 0
            else: self.active = 1
            
            return msg + f'\n {self.players[self.active]} wins!'

        if sum(self.board) == 13:
            return msg + '\n It\'s a draw!'

        return f'{self.players[self.active]}\n' + msg

    def edit(self, reaction):
        reaction = str(reaction)

        # Parse reaction
        move = -1
        if reaction == '1️⃣': move = 1
        if reaction == '2️⃣': move = 2
        if reaction == '3️⃣': move = 3

        if reaction == '4️⃣': move = 4
        if reaction == '5️⃣': move = 5
        if reaction == '6️⃣': move = 6

        if reaction == '7️⃣': move = 7
        if reaction == '8️⃣': move = 8
        if reaction == '9️⃣': move = 9

        if move == -1:
            return None

        # If empty space, place tile
        if self.board[move - 1] == 0:
            self.board[move - 1] = self.active + 1

            # Toggle active player
            if self.active == 1: self.active = 0
            else: self.active = 1

        return self.display()