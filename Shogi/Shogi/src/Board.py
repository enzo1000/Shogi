import pygame
from pieces.Pieces import *
from .constants import *

class Board:
    def __init__ (self, widthS, heightS, rows, cols, square, window):
        self.width = widthS
        self.height = heightS
        self.row = rows
        self.col = cols
        self.square = square
        self.window = window
        self.Board = []
        self.createBoard()

    def createBoard(self):
        for row in range(self.row): #Pour chacune des lignes de notre plateau
            self.Board.append([0 for i in range (self.col)])    #On vient créer le nombre de cases pour la ligne correspondante

            for col in range (self.col):    #Celon la position (indice) on ajoute une pièce en particulier
                if row == 2:    #Toute les cases de la ligne 2 deviennent des pions Reignant
                    self.Board[row][col] = Pieces.Pion(self.square, imagesPiecesReignant["pion"], Joueur.Regnant, "Pion", row, col)

                if row == 6:
                    self.Board[row][col] = Pieces.Pion(self.square, imagesPiecesOpposant["pion"], Joueur.Opposant, "Pion", row, col)

                if row == 1:    #Tour et fou coté régnant
                    if col == 1:
                        pass
                    if col == 6:
                        pass

                if row == 7:    #Idem coté opposant
                    if col == 1:
                        pass
                    if col == 6:
                        pass

                if row == 0:    #Pieces du régnant
                    pass

                if row == 8:    #Pieces de l'opposant
                    pass


