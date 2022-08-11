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
        for self.row in range(self.row): #Pour chacune des lignes de notre plateau
            self.Board.append([0 for i in range (self.col)])    #On vient créer le nombre de cases pour la ligne correspondante

            for self.col in range (self.col):    #Celon la position (indice) on ajoute une pièce en particulier
                if row == 1:    #Toute les cases de la ligne 1 deviennent des pions
                    self.Board[row][col] = Pion(self.square, pion, Reignant, "Pion", row, col)
                        #Premier pb : la rotation des images
                        #Deuxième pb : le coté Reignant ou Opposant est un enum ou un string ?(string plus facile mais enum plus pro)

