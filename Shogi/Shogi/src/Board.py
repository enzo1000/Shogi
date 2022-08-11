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
            self.Board.append([0 for i in range (self.col)])    #On vient cr�er le nombre de cases pour la ligne correspondante

            for col in range (self.col):    #Celon la position (indice) on ajoute une pi�ce en particulier

                if row == 2:    #Toute les cases de la ligne 2 deviennent des pions Reignant
                    self.Board[row][col] = Pieces.Pion(self.square, imagesPiecesReignant["pion"], Joueur.Regnant, "Pion", row, col)

                if row == 6:    #Idem cot� Opposant
                    self.Board[row][col] = Pieces.Pion(self.square, imagesPiecesOpposant["pion"], Joueur.Opposant, "Pion", row, col)

                if row == 1:    #Tour et fou cot� r�gnant
                    if col == 1:
                        self.Board[row][col] = Pieces.Tour(self.square, imagesPiecesReignant["tour"], Joueur.Regnant, "Tour", row, col)
                    if col == 6:
                        self.Board[row][col] = Pieces.Fou(self.square, imagesPiecesReignant["fou"], Joueur.Regnant, "Fou", row, col)

                if row == 7:    #Idem cot� opposant
                    if col == 1:
                        self.Board[row][col] = Pieces.Fou(self.square, imagesPiecesOpposant["fou"], Joueur.Opposant, "Fou", row, col)
                    if col == 6:
                        self.Board[row][col] = Pieces.Tour(self.square, imagesPiecesOpposant["tour"], Joueur.Opposant, "Tour", row, col)

                if row == 0:    #Pieces du r�gnant
                    if col == 0 or col == 8:
                        self.Board[row][col] = Pieces.Lancier(self.square, imagesPiecesReignant["lancier"], Joueur.Regnant, "Lancier", row, col)
                    if col == 1 or col == 7:
                        self.Board[row][col] = Pieces.Cavalier(self.square, imagesPiecesReignant["cavalier"], Joueur.Regnant, "Cavalier", row, col)
                    if col == 2 or col == 6:
                        self.Board[row][col] = Pieces.GeneralDargent(self.square, imagesPiecesReignant["generalDargent"], Joueur.Regnant, "GeneralDargent", row, col)
                    if col == 3 or col == 5:
                        self.Board[row][col] = Pieces.GeneralDor(self.square, imagesPiecesReignant["generalDor"], Joueur.Regnant, "GeneralDor", row, col)
                    if col == 4:
                        self.Board[row][col] = Pieces.Roi(self.square, imagesPiecesReignant["roi"], Joueur.Regnant, "Roi", row, col)

                if row == 8:    #Pieces de l'opposant
                    if col == 0 or col == 8:
                        self.Board[row][col] = Pieces.Lancier(self.square, imagesPiecesOpposant["lancier"], Joueur.Opposant, "Lancier", row, col)
                    if col == 1 or col == 7:
                        self.Board[row][col] = Pieces.Cavalier(self.square, imagesPiecesOpposant["cavalier"], Joueur.Opposant, "Cavalier", row, col)
                    if col == 2 or col == 6:
                        self.Board[row][col] = Pieces.GeneralDargent(self.square, imagesPiecesOpposant["generalDargent"], Joueur.Opposant, "GeneralDargent", row, col)
                    if col == 3 or col == 5:
                        self.Board[row][col] = Pieces.GeneralDor(self.square, imagesPiecesOpposant["generalDor"], Joueur.Opposant, "GeneralDor", row, col)
                    if col == 4:
                        self.Board[row][col] = Pieces.Roi(self.square, imagesPiecesOpposant["roi"], Joueur.Opposant, "Roi", row, col)

        def getPiece(self, row, col):
            return self.Board[row][col]

        def move(self, piece, row, col):
            #Ecriture python de changement de 2 valeurs sur une m�me ligne sans passer par une 3eme variable tampon
            self.Board[piece.row, piece.col], self.Board[row][col] = self.Board[row][col], self.Board[piece.row][piece.col]
            piece.pieceMove(row, col)

        def drawBoard(self):
            self.Win.fill(brown)
            for row in range(self.row):
                for col in range(row%2, self.col, 2):
                    pygame.draw.rect(self.Win, White, (square*(row), square*(col), square, square))

        def drawPiece(self, piece, Win):
            Win.blit(piece.image, (piece.x, piece.y))

        def drawPieces(self):
            for row in range(self.row):
                for col in range(self.col):
                    if self.Board[row][col] != 0:
                        self.drawPiece(self.Board[row][col], self.Win)
