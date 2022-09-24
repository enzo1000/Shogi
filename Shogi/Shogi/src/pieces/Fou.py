from .Pieces import *

class Fou(Pieces):
    
    def __init__(self, square, image, cote, type, row, col):
        super().__init__(square, image, cote, type, row, col)

    def getAvailableMoves(self, row, col, Board):
        self.clearAvailableMoves()

        rowi = row + 1  #Cette fois le mec de la video prefere passer par d autres variables
        coli = col + 1  #C est pas une mauvaise idee mais c est pas necessaire non plus, bref

        while rowi < len(Board) and coli < len(Board[row]):
            if Board[rowi][coli] == 0:
                self.availableMoves.append((rowi, coli))
                rowi += 1
                coli += 1

            elif Board[rowi][coli].cote != self.cote:
                self.availableMoves.append((rowi, coli))
                break
            break

        rowi = row - 1
        coli = col - 1

        while rowi >= 0 and coli >= 0:
            if Board[rowi][coli] == 0:
                    self.availableMoves.append((rowi, coli))
                    rowi -= 1
                    coli -= 1

            elif Board[rowi][coli].cote != self.cote:
                self.availableMoves.append((rowi, coli))
                break
            break

        rowi = row + 1
        coli = col - 1

        while rowi < len(Board) and coli >= 0:
            if Board[rowi][coli] == 0:
                    self.availableMoves.append((rowi, coli))
                    rowi += 1
                    coli -= 1

            elif Board[rowi][coli].cote != self.cote:
                self.availableMoves.append((rowi, coli))
                break
            break

        rowi = row - 1
        coli = col + 1

        while rowi >= 0 and coli < len(Board[row]):
            if Board[rowi][coli] == 0:
                    self.availableMoves.append((rowi, coli))
                    rowi -= 1
                    coli += 1

            elif Board[rowi][coli].cote != self.cote:
                self.availableMoves.append((rowi, coli))
                break
            break

        return self.availableMoves