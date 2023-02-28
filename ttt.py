import os

DEBUG = False

translator = {
            0: "_",
            1: "X",
            2: "O"
        }

def clearScreen():
    os.system("clear")

def winCondition(r, v): # row table and associated value
    if r[0][0] == r[1][1] == r[2][2] == v: return True
    for row in r:
        if row[0] == row[1] == row[2] == v: return True
    for c in range(len(r)):
        if r[0][c] == r[1][c] == r[2][c]: return True
    return False

class TicTacToeBoard:
    def __init__(self):
        self.rows = [[0 for r in range(3)] for c in range(3)]  
        
    def __repr__(self):
        return "<TicTacToeBoard " + str(self.rows) + ">"
        
    def __str__(self):
        return "\n".join([" ".join([translator[x] for x in self[r]]) for r in range(3)])
        
    def __getitem__(self, row):
        return self.rows[row]
        
    def setVal(self, row, column, value):
        if self[row][column] != 0:
            raise SyntaxError("Space already taken.")
        self[row][column] = value
        
    def setX(self, row, column):
        if self[row][column] != 0:
            raise SyntaxError("Space already taken.")
        self[row][column] = 1
        
    def setO(self, row, column):
        if self[row][column] != 0:
            raise SyntaxError("Space already taken.")
        self[row][column] = 2
        
    def hasXWon(self):
        return winCondition(self.rows, 1)
        
    def hasOWon(self):
        return winCondition(self.rows, 2)
        
class Game(TicTacToeBoard):
	def __init__(self):
        TicTacToeBoard.__init__(self)
        self.winner = 0
        self.turn = 0
		
class MultiplayerGame(Game):
    def startGame(self, startingPlayer=1, debug=False):
        self.turn = startingPlayer
        
        while not self.hasXWon() or self.hasOWon():
            clearScreen()
            print(translator[self.turn] + "\'s turn (value: " + str(self.turn) + ")")
            print(str(self))
            try:
                r = int(input("row: ")) -1
                c = int(input("col: ")) -1
                self.setVal(r, c, self.turn)
                if self.turn == 1:
                    if debug: input("turn was 1, setting to 2")
                    self.turn = 2
                elif self.turn == 2:
                    if debug: input("turn was 2, setting to 1")
                    self.turn = 1
                else:
                    clearScreen()
                    print("game reached a theoretically unreachable state. sorry!")
            except ValueError:
                input("error: invalid row/column input. (<Enter> to continue)")
                
            except IndexError:
                input("error: invalid row/column number. (<Enter> to continue)")
            
            except SyntaxError:
                input("error: spot already taken. (<Enter> to continue)")

        clearScreen()
        if self.turn == 1:
            if debug: input("turn was 1, setting to 2")
            self.turn = 2
        elif self.turn == 2:
            if debug: input("turn was 2, setting to 1")
            self.turn = 1
        else:
            clearScreen()
            print("game reached a theoretically unreachable state. sorry!")
        print(translator[self.turn] + " won")
		self.winner = self.turn
		return self.winner
	
class AIGame:
	def startGame(self, startingPlayer=1, debug=False):
        self.turn = startingPlayer
        
        while not self.hasXWon() or self.hasOWon():
            clearScreen()
            print("human\'s turn (value: " + str(self.turn) + ")")
            print(str(self))
            try:
                r = int(input("row: ")) -1
                c = int(input("col: ")) -1
                self.setVal(r, c, self.turn)
                if self.turn == 1:
                    if debug: input("turn was 1, setting to 2")
                    self.turn = 2
                elif self.turn == 2:
                    if debug: input("turn was 2, setting to 1")
                    self.turn = 1
                else:
                    clearScreen()
                    print("game reached a theoretically unreachable state. sorry!")
            except ValueError:
                input("error: invalid row/column input. (<Enter> to continue)")
                
            except IndexError:
                input("error: invalid row/column number. (<Enter> to continue)")
            
            except SyntaxError:
                input("error: spot already taken. (<Enter> to continue)")

        clearScreen()
        if self.turn == 1:
            if debug: input("turn was 1, setting to 2")
            self.turn = 2
        elif self.turn == 2:
            if debug: input("turn was 2, setting to 1")
            self.turn = 1
        else:
            clearScreen()
            print("game reached a theoretically unreachable state. sorry!")
        print(translator[self.turn] + " won")
		self.winner = self.turn
		return self.winner

if __name__ == "__main__":
	MultiplayerGame().startGame(debug=DEBUG)
