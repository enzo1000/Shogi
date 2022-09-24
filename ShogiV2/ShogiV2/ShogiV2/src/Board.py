import pygame
from .Pieces import *
from .constants import *

class Board:
    def __init__ (self, Width, Height, rows, cols, square, window):
        self.width = Width
        self.height = Height
        self.row = rows
        self.col = cols
        self.square = square
        self.window = window
        self.padding = 6
        self.Board = []
        self.Side = []
        self.createBoard()
        self.createSide()
        
    def createBoard(self):
        for row in range(self.row):
            self.Board.append([0 for i in range (self.col)])

            for col in range (self.col):

                if row == 2:
                    self.Board[row][col] = Pion(self.square, imagesPiecesRegnant["pion"], Joueur.Regnant, "Pion", row, col)

                if row == 6:
                    self.Board[row][col] = Pion(self.square, imagesPiecesOpposant["pion"], Joueur.Opposant, "Pion", row, col)

                if row == 1:
                    if col == 1:
                        self.Board[row][col] = Tour(self.square, imagesPiecesRegnant["tour"], Joueur.Regnant, "Tour", row, col)
                    if col == 7:
                        self.Board[row][col] = Fou(self.square, imagesPiecesRegnant["fou"], Joueur.Regnant, "Fou", row, col)

                if row == 7:
                    if col == 1:
                        self.Board[row][col] = Fou(self.square, imagesPiecesOpposant["fou"], Joueur.Opposant, "Fou", row, col)
                    if col == 7:
                        self.Board[row][col] = Tour(self.square, imagesPiecesOpposant["tour"], Joueur.Opposant, "Tour", row, col)

                if row == 0:
                    if col == 0 or col == 8:
                        self.Board[row][col] = Lancier(self.square, imagesPiecesRegnant["lancier"], Joueur.Regnant, "Lancier", row, col)
                    if col == 1 or col == 7:
                        self.Board[row][col] = Cavalier(self.square, imagesPiecesRegnant["cavalier"], Joueur.Regnant, "Cavalier", row, col)
                    if col == 2 or col == 6:
                        self.Board[row][col] = GeneralDargent(self.square, imagesPiecesRegnant["generalDargent"], Joueur.Regnant, "GeneralDargent", row, col)
                    if col == 3 or col == 5:
                        self.Board[row][col] = GeneralDor(self.square, imagesPiecesRegnant["generalDor"], Joueur.Regnant, "GeneralDor", row, col)
                    if col == 4:
                        self.Board[row][col] = Roi(self.square, imagesPiecesRegnant["roi"], Joueur.Regnant, "Roi", row, col)

                if row == 8:
                    if col == 0 or col == 8:
                        self.Board[row][col] = Lancier(self.square, imagesPiecesOpposant["lancier"], Joueur.Opposant, "Lancier", row, col)
                    if col == 1 or col == 7:
                        self.Board[row][col] = Cavalier(self.square, imagesPiecesOpposant["cavalier"], Joueur.Opposant, "Cavalier", row, col)
                    if col == 2 or col == 6:
                        self.Board[row][col] = GeneralDargent(self.square, imagesPiecesOpposant["generalDargent"], Joueur.Opposant, "GeneralDargent", row, col)
                    if col == 3 or col == 5:
                        self.Board[row][col] = GeneralDor(self.square, imagesPiecesOpposant["generalDor"], Joueur.Opposant, "GeneralDor", row, col)
                    if col == 4:
                        self.Board[row][col] = GeneralDeJade(self.square, imagesPiecesOpposant["generalDeJade"], Joueur.Opposant, "GeneralDeJade", row, col)

    def createSide(self):
        for row in range(self.row):
            self.Side.append([0 for i in range(self.col + 3)])
            for col in range(self.col + 2):

                if row == 0:
                    if col == self.col + 0:
                        self.Side[row][col] = GeneralDor(self.square, imagesPiecesOpposant["generalDor"], Joueur.Opposant, "GeneralDor", row, col)
                    elif col == self.col + 1:
                        self.Side[row][col] = GeneralDargent(self.square, imagesPiecesOpposant["generalDargent"], Joueur.Opposant, "GeneralDargent", row, col)

                if row == 1:
                    if col == self.col + 0:
                        self.Side[row][col] = Lancier(self.square, imagesPiecesOpposant["lancier"], Joueur.Opposant, "Lancier", row, col)
                    elif col == self.col + 1:
                        self.Side[row][col] = Cavalier(self.square, imagesPiecesOpposant["cavalier"], Joueur.Opposant, "Cavalier", row, col)

                if row == 2:
                    if col == self.col + 0:
                        self.Side[row][col] = Tour(self.square, imagesPiecesOpposant["tour"], Joueur.Opposant, "Tour", row, col)
                    elif col == self.col + 1:
                        self.Side[row][col] = Fou(self.square, imagesPiecesOpposant["fou"], Joueur.Opposant, "Fou", row, col)

                if row == 3:
                    if col == self.col + 0:
                        self.Side[row][col] = Pion(self.square, imagesPiecesOpposant["pion"], Joueur.Opposant, "Pion", row, col)

    def getPiece(self, row, col):
        return self.Board[row][col]

    def getSideType(self, row, col):
        return self.Side[row][col]
    
    def move(self, piece, row, col):
        self.Board[piece.row][piece.col], self.Board[row][col] = self.Board[row][col], self.Board[piece.row][piece.col]
        piece.pieceMove(row, col)

    def drawBoard(self):
        self.window.fill(brown)
        for row in range(self.row):
            for col in range(row%2, self.col, 2):
                pygame.draw.rect(self.window, white, (square*(row), square*(col), square, square))

    def drawPiece(self, piece, Win):
        Win.blit(piece.image, (piece.x, piece.y))

    def drawSide(self):
        for row in range(self.row):
            for col in range(self.col + 2):
                if self.Side[row][col] != 0:
                    self.drawPiece(self.Side[row][col], self.window)

    def drawPieces(self):
        for row in range(self.row):
            for col in range(self.col):
                if self.Board[row][col] != 0:
                    self.drawPiece(self.Board[row][col], self.window)
