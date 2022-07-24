from Pieces import *

class Cavalier(Pieces):
    def __init__(self, square, image, cote, type, row, col):
        super().__init__(square, image, cote, type, row, col)

    def getAvailableMoves(self, row, col, Board):
        self.clearAvailableMoves()

        if self.cote == Regnant:            #Si Regnant alors joueur est en bas du plateau
            if row - 2 >= 0 and col + 1 < len(Board):
                if Board[row-2][col+1] == 0 or Board[row-2][col+1].cote != self.cote:
                    self.availableMoves.append((row-2, col+1))

            if row - 2 >= 0 and col - 1 >= 0:
                if Board[row-2][col-1] == 0 or Board[row-2][col-1].cote != self.cote:
                    self.availableMoves.append((row-2, col-1))

        if self.cote == Opposant:   
            if row + 2 < len(Board[row]) and col + 1 < len(Board):
                if Board[row+2][col+1] == 0 or Board[row-2][col+1].cote != self.cote:
                    self.availableMoves.append((row+2, col+1))

            if row + 2 < len(Board[row]) and col - 1 >= 0:
                if Board[row+2][col-1] == 0 or Board[row+2][col-1].cote != self.cote:
                    self.availableMoves.append((row+2, col-1))

        return self.availableMoves