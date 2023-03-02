import blessed
import time
import sys

DEBUG = True

EMPTY = "_"
X = "X"
O = "O"

DIMENSION = 3

temp = [[(x, y) for y in range(DIMENSION)] for x in range(DIMENSION)]
COORDINATES = []
for l in temp:
    for d in l:
        COORDINATES.append(d)
print(COORDINATES)

def opponent(player: X or O):
    if player == X:
        return O 
    return X

class Board:
    def __init__(self, board: list[list[EMPTY or X or O]]=[[EMPTY for _ in range(DIMENSION)] for _ in range(DIMENSION)]) -> None:
        """Initialize the Board object."""
        self.board = board

    def __getitem__(self, coords: tuple[int, int]) -> X or O or EMPTY:
        return self.board[coords[0]][coords[1]]

    def __setitem__(self, coords: tuple[int, int], value: X or O) -> None:
        self.board[coords[0]][coords[1]] = value

    def __str__(self) -> str:
        return "\t 0\t 1\t 2\n" + "\n\n".join([str(x) + "\t|" + "|\t|".join(self.board[x]) + "|" for x in range(DIMENSION)])

    def __repr__(self) -> str:
        return str(self)

    def __contains__(self, item) -> bool:
        for row in self.board:
            if item in row:
                return True
        return False

    def checkWin(self, player: str) -> bool:
        """Check if a player has won the game."""
        for row in range(DIMENSION):
            if self[(row, 0)] == self[(row, 1)] == self[(row, 2)] == player:
                return True
        
        for col in range(DIMENSION):
            if self[(0, col)] == self[(1, col)] == self[(2, col)] == player:
                return True

        if self[(0, 0)] == self[(1, 1)] == self[(2, 2)] == player:
            return True

        if self[(0, 2)] == self[(1, 1)] == self[(2, 0)] == player:
            return True

        return False

    def checkTie(self) -> bool:
        """Check if the game's been tied."""
        return (EMPTY not in self) and (not (self.checkWin(X) or self.checkWin(O)))

    def checkFinished(self) -> bool:
        """Check if the game's finished at all."""
        return self.checkWin(X) or self.checkWin(O) or self.checkTie()

    def isEmpty(self, coords: tuple[int, int]) -> bool:
        """Check if the specified space on the board is empty."""
        return self[coords] == EMPTY

    def place(self, player: X or O, coords: tuple[int, int]) -> bool:
        """Put down a piece, X or O, at the specified coordinates."""
        if not (0 <= coords[0] < DIMENSION and 0 <= coords[1] < DIMENSION):
            raise SyntaxError("Coordinate indices out of range.")
        if self.isEmpty(coords):
            self[coords] = player
            return True
        return False

    def theorize(self, player: X or O, coords: tuple[int, int]) -> object:
        """Return a new Board state after making a new move."""
        b = Board(self.board)
        if b.place(player, coords):
            return b
        return None

    def getPossibleMoves(self) -> list[object]:
        """Return a list of Boards that the player can get to from here in one move."""
        return [coordinate for coordinate in COORDINATES if self.isEmpty(coordinate)]

    def getScore(self, player: X or O, invert=True) -> int:
        """Use a minimax algorithm to determine the value of the board state for the given player."""

        if self.checkWin(player):
            return 1
        elif self.checkWin(opponent(player)):
            return -1
        elif self.checkTie():
            return 0
        
        score = sum([self.theorize(coordinate).getScore(opponent(player), invert=not invert) for coordinate in self.getPossibleMoves])
        if invert:
            return -1 * score
        else:
            return score
    
    def pvp(self) -> None:
        """Play against someone else."""

        term = blessed.Terminal()

        turn = O

        while not self.checkFinished():
            print(term.clear())
            turn = opponent(turn)

            print(turn + "\'s Turn")
            print(self)
            while True:
                try:
                    row = int(input("Enter row: "))
                    try:
                        col = int(input("Enter col: "))
                    except KeyboardInterrupt:
                        continue
                    if self.place(turn, (row, col)):
                        break
                    input("Space already taken (<Enter> to continue)")
                except ValueError:
                    input("Not a valid space (<Enter> to continue)")

        if self.checkWin(X):
            print("X won!")
        elif self.checkWin(O):
            print("O won!")
        else:
            print("Tie.")

    def pve(self) -> None:
        term = blessed.Terminal()

        while not self.checkFinished():
            print(term.clear())
            print("Human\'s Turn")
            print(self)
            while True:
                try:
                    row = int(input("Enter row: "))
                    try:
                        col = int(input("Enter col: "))
                    except KeyboardInterrupt:
                        continue
                    if self.place(X, (row, col)):
                        break
                    input("Space already taken (<Enter> to continue)")
                except ValueError:
                    input("Not a valid space (<Enter> to continue)")

            print(term.clear())
            print("Khan\'s Turn")
            print("Thinking ...")

            possibleMoves = self.getPossibleMoves()
            if DEBUG: 
                print(possibleMoves)
                input()
            boards = [self.theorize(O, coordinate) for coordinate in possibleMoves]
            boards = [board for board in boards if board is not None]
            if DEBUG: 
                print(self)
                input()

            scores = {boards[x].getScore(O, False): possibleMoves[x] for x in range(len(possibleMoves))}
            self.place(O, scores[max(scores.keys())])

        if self.checkWin(X):
            print("X won!")
        elif self.checkWin(O):
            print("O won!")
        else:
            print("Tie.")