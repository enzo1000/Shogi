from .Pieces import *

class Roi(Pieces):
    def __init__(self, square, image, cote, type, row, col):
        super().__init__(square, image, cote, type, row, col)

    #Fonction qui pour une ligne donnee, donne les mouvements possibles en parcourant les 3 cases en face de ladite piece
    #Pour expliquer plus simplement, le roi il peut aller partout case par case, avec cette fonction, on simplifie en memoire le calcul des mouvements
    # pour la ligne en haut du roi, celle du mileu (en supprimant la case du roi) et en bas du roi
    def kingLigneHautBas(self, rowi, Board):
        for coli in [self.col-1, self.col, self.col+1]:     #On fait la ligne du haut en premier (les 3 cases en haut de la piece)
            if coli != self.col or rowi != self.row:       #Pour eviter de pouvoir faire bouger le roi sur lui meme (sur place)
                if Board[rowi][coli] >= 0 and Board[rowi][coli] < len(Board[self.row]):   #Si on ne deborde pas alors 
                    if Board[rowi][coli] == 0:
                        self.availableMoves.append((rowi, coli))
                    elif Board[rowi][coli].cote != self.cote:
                        self.availableMoves.append((rowi, coli))
        
    def getAvailableMoves(self, row, col, Board):
        self.clearAvailableMoves()

        self.kingLigneHautBas(self, row - 1, Board)
        self.kingLigneHautBas(self, row, Board)
        self.kingLigneHautBas(self, row + 1, Board)
        return self.availableMoves
