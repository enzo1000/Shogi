from .Pieces import *

class GeneralDor(Pieces):
    def __init__(self, square, image, cote, type, row, col):
        super().__init__(square, image, cote, type, row, col)

    def generalLigneHautBas(self, rowi, Board):
         for coli in [self.col-1, self.col, self.col+1]:     #On fait la ligne du haut en premier (les 3 cases en haut de la piece)
             if coli != self.col or rowi != self.row:
                if Board[rowi][coli] >= 0 and Board[rowi][coli] < len(Board[self.row]):   #Si on ne déborde pas alors 
                    if Board[rowi][coli] == 0:
                        self.availableMoves.append((rowi, coli))
                    elif Board[rowi][coli].cote != self.cote:
                        self.availableMoves.append((rowi, coli))

    def getAvailableMoves(self, row, col, Board):
        self.clearAvailableMoves()

        if self.cote == Joueur.Opposant:
            self.generalLigneHautBas(self, row - 1, Board)
            self.generalLigneHautBas(self, row, Board)
            if Board[row + 1][col] == 0:
                self.availableMoves.append((row + 1, col))

        else:
            self.generalLigneHautBas(self, row + 1, Board)
            self.generalLigneHautBas(self, row, Board)
            if Board[row - 1][col] == 0:
                self.availableMoves.append((row - 1, col))



