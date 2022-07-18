from Pieces import *

#Classe Pion hérite de la classe Piece
class Tour(Pieces): 

    def __init__(self, square, image, cote, type, row, col):
        super().__init__(square, image, cote, type, row, col)

    def getAvailableMoves(self, row, col, Board):
        self.clearAvailableMoves()

        for i in range(row+1, len(Board)): #Vers le bas jusqu'au bors du tableau

            if Board[i][col] == 0:
                self.availableMoves.append((i, col))

            elif Board[i][col].cote != self.color:
                self.availableMoves.append((i, col))
                break

            break

        for j in range(row-1, -1, -1):  #On va de row-1 à -1 avec un pas de -1 par -1 (-1 exclue) vers le haut

            if Board[j][col] == 0:
                self.availableMoves.append((j, col))

            elif Board[j][col].cote != self.color:
                self.availableMoves.append((j, col))
                break

            break

        for k in range(col+1, len(Board[row])): #On va vers la droite

            if Board[row][k] == 0:
                self.availableMoves.append((row, k))

            elif Board[row][k].cote != self.color:
                self.availableMoves.append((row, k))
                break

            break

        for l in range(col-1, -1, -1):  #On va de col-1 à -1 avec un pas de -1 par -1 (-1 exclue) vers la gauche

            if Board[row][l] == 0:
                self.availableMoves.append((row, l))

            elif Board[row][l].cote != self.color:
                self.availableMoves.append((row, l))
                break

            break

        return self.availableMoves