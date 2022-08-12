from Pieces import *

class GeneralDor(Pieces):
    def __init__(self, square, image, cote, type, row, col):
        super().__init__(square, image, cote, type, row, col)

    def getAvailableMoves(self, row, col, Board):
        for coli in [self.col-1, self.col, self.col+1]:     #On fait la ligne du haut en premier (les 3 cases en haut de la piece)
            if Board[row][coli] >= 0 and Board[row][coli] < len(Board[self.row]):   #Si on ne déborde pas alors 
                if Board[row][coli] == 0:
                    self.availableMoves.append((row, coli))
                elif Board[row][coli].cote != self.cote:
                    self.availableMoves.append((row, coli))



