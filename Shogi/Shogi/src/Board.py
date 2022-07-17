import pygame
from .Pieces import *
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
                pass
