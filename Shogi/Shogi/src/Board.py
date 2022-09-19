import pygame
from .pieces.Pieces import *
from .pieces import *
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

    #Attribut à chaques cases du plateau les pièces adéquates à un début de partie
    def createBoard(self):
        for row in range(self.row): #Pour chacune des lignes de notre plateau
            self.Board.append([0 for i in range (self.col)])    #On vient créer le nombre de cases pour la ligne correspondante

            for col in range (self.col):    #Celon la position (indice) on ajoute une pièce en particulier

                if row == 2:    #Toute les cases de la ligne 2 deviennent des pions Reignant
                    self.Board[row][col] = Pieces.Pion(self.square, imagesPiecesRegnant["pion"], Joueur.Regnant, "Pion", row, col)

                if row == 6:    #Idem coté Opposant
                    self.Board[row][col] = Pieces.Pion(self.square, imagesPiecesOpposant["pion"], Joueur.Opposant, "Pion", row, col)

                if row == 1:    #Tour et fou coté régnant
                    if col == 1:
                        self.Board[row][col] = Pieces.Tour(self.square, imagesPiecesRegnant["tour"], Joueur.Regnant, "Tour", row, col)
                    if col == 7:
                        self.Board[row][col] = Pieces.Fou(self.square, imagesPiecesRegnant["fou"], Joueur.Regnant, "Fou", row, col)

                if row == 7:    #Idem coté opposant
                    if col == 1:
                        self.Board[row][col] = Pieces.Fou(self.square, imagesPiecesOpposant["fou"], Joueur.Opposant, "Fou", row, col)
                    if col == 7:
                        self.Board[row][col] = Pieces.Tour(self.square, imagesPiecesOpposant["tour"], Joueur.Opposant, "Tour", row, col)

                if row == 0:    #Pieces du régnant
                    if col == 0 or col == 8:
                        self.Board[row][col] = Pieces.Lancier(self.square, imagesPiecesRegnant["lancier"], Joueur.Regnant, "Lancier", row, col)
                    if col == 1 or col == 7:
                        self.Board[row][col] = Pieces.Cavalier(self.square, imagesPiecesRegnant["cavalier"], Joueur.Regnant, "Cavalier", row, col)
                    if col == 2 or col == 6:
                        self.Board[row][col] = Pieces.GeneralDargent(self.square, imagesPiecesRegnant["generalDargent"], Joueur.Regnant, "GeneralDargent", row, col)
                    if col == 3 or col == 5:
                        self.Board[row][col] = Pieces.GeneralDor(self.square, imagesPiecesRegnant["generalDor"], Joueur.Regnant, "GeneralDor", row, col)
                    if col == 4:
                        self.Board[row][col] = Pieces.Roi(self.square, imagesPiecesRegnant["roi"], Joueur.Regnant, "Roi", row, col)

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
                        self.Board[row][col] = Pieces.GeneralDeJade(self.square, imagesPiecesOpposant["generalDeJade"], Joueur.Opposant, "GeneralDeJade", row, col) #Ici on aurait aussi pu utiliser un roi

    #Place les pièces dans le tableau Side
    def createSide(self):
        for row in range(self.row):
            self.Side.append([0 for i in range(self.col + 3)])
            for col in range(self.col + 2):

                if row == 0:
                    if col == self.col + 0:
                        self.Side[row][col] = Pieces.GeneralDor(self.square, imagesPiecesOpposant["generalDor"], Joueur.Opposant, "GeneralDor", row, col)
                    elif col == self.col + 1:
                        self.Side[row][col] = Pieces.GeneralDargent(self.square, imagesPiecesOpposant["generalDargent"], Joueur.Opposant, "GeneralDargent", row, col)

                if row == 1:
                    if col == self.col + 0:
                        self.Side[row][col] = Pieces.Lancier(self.square, imagesPiecesOpposant["lancier"], Joueur.Opposant, "Lancier", row, col)
                    elif col == self.col + 1:
                        self.Side[row][col] = Pieces.Cavalier(self.square, imagesPiecesOpposant["cavalier"], Joueur.Opposant, "Cavalier", row, col)

                if row == 2:
                    if col == self.col + 0:
                        self.Side[row][col] = Pieces.Tour(self.square, imagesPiecesOpposant["tour"], Joueur.Opposant, "Tour", row, col)
                    elif col == self.col + 1:
                        self.Side[row][col] = Pieces.Fou(self.square, imagesPiecesOpposant["fou"], Joueur.Opposant, "Fou", row, col)

                if row == 3:
                    if col == self.col + 0:
                        self.Side[row][col] = Pieces.Pion(self.square, imagesPiecesOpposant["pion"], Joueur.Opposant, "Pion", row, col)

    #Retourne la pièce sur la case aux coordonnées données
    #Retourne 0 si la case est "vide" (ne contient pas de pièce)
    def getPiece(self, row, col):
        return self.Board[row][col]

    def getSideType(self, row, col):
        return self.Side[row][col]

    #Déplace une pièce à partir de sa position actuelle et sa nouvelle position en paramètre
    def move(self, piece, row, col):
        #Ecriture python de changement de 2 valeurs sur une même ligne sans passer par une 3eme variable tampon
        self.Board[piece.row][piece.col], self.Board[row][col] = self.Board[row][col], self.Board[piece.row][piece.col]
        piece.pieceMove(row, col)   #On vient actualiser le placement de la pièce (row, col et x, y)

    #Construit le terrain avec un fond marron et des cases blanches
    def drawBoard(self):
        self.window.fill(brown)                     #Toute la fenêtre en marron
        for row in range(self.row):                 #Pour toutes les lignes
            for col in range(row%2, self.col, 2):   #Pour, si la colonne est pair ou impaire (couleur de la première case sur la ligne), la dernière col, une marche de 1 case sur 2
                pygame.draw.rect(self.window, white, (square*(row), square*(col), square, square))

    #Place une pièce à une coordonée donné
    def drawPiece(self, piece, Win):
        Win.blit(piece.image, (piece.x, piece.y))

    #Actualise les pièces coté side
    def drawSide(self):
        for row in range(self.row):
            for col in range(self.col + 2):
                if self.Side[row][col] != 0:
                    self.drawPiece(self.Side[row][col], self.window)

    #Avec l'utilisation de drawPiece permet d'actualiser toutes les pièces sur le terrain
    def drawPieces(self):
        for row in range(self.row):
            for col in range(self.col):
                if self.Board[row][col] != 0:
                    self.drawPiece(self.Board[row][col], self.window)
