from .Pieces import *

class Lancier(Pieces):
    def __init__(self, square, image, cote, type, row, col):
        super().__init__(square, image, cote, type, row, col)

    def getAvailableMoves(self, row, col, Board):
        self.clearAvailableMoves()

        if self.cote == Joueur.Regnant:            #Si Regnant alors joueur est en bas du plateau
            for j in range(row-1, -1, -1):  #Vers le haut du plateau

                if Board[j][col] == 0:
                    self.availableMoves.append((j, col))

                elif Board[j][col].cote != self.color:
                    self.availableMoves.append((j, col))
                    break
                break
            

        if self.cote == Joueur.Opposant:   
            for i in range(row+1, len(Board)): #Vers le bas jusqu'au bors du tableau

                if Board[i][col] == 0:
                    self.availableMoves.append((i, col))

                elif Board[i][col].cote != self.color:
                    self.availableMoves.append((i, col))
                    break
                break




