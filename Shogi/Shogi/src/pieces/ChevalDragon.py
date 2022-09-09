from .Pieces import *

class ChevalDragon(Pieces):
    def __init__(self, square, image, cote, type, row, col):
        super().__init__(square, image, cote, type, row, col)

    def kingLigneHautBas(self, rowi, Board):
        for coli in [self.col-1, self.col, self.col+1]:     #On fait la ligne du haut en premier (les 3 cases en haut de la piece)
            if coli != self.col or rowi != self.row:       #Pour éviter de pouvoir faire bouger le roi sur lui même (sur place)
                if Board[rowi][coli] >= 0 and Board[rowi][coli] < len(Board[self.row]):   #Si on ne déborde pas alors 
                    if Board[rowi][coli] == 0:
                        self.availableMoves.append((rowi, coli))
                    elif Board[rowi][coli].cote != self.cote:
                        self.availableMoves.append((rowi, coli))

    def getAvailableMoves(self, row, col, Board):
        self.clearAvailableMoves()

        self.kingLigneHautBas(self, row - 1, Board)
        self.kingLigneHautBas(self, row, Board)
        self.kingLigneHautBas(self, row + 1, Board)

        rowi = row + 1  #Cette fois le mec de la vidéo préfère passer par d'autres variables
        coli = col + 1  #C'est pas une mauvaise idée mais c'est pas nécessaire non plus, bref

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




