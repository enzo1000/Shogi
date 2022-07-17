import pygame

from .constants import *

class Piece:    #On créer une classe Piece
    def __init__(self, square, image, cote, type, row, col):   #Constructeur prenant
        self.square = square    #Dimension ?
        self.image = image      #Image de la piece
        self.cote = cote        #Si le joueur a un roi ou un général de jade    (Regnant ou Opposant)
        self.row = row          #Position ligne ?
        self.col = col          #Position colonne ?
        self.type = type        #Type (roi, cavalier ...)
        self.x = 0              #Je ne sais pas
        self.y = 0              #Idem
        self.availableMoves = []   #Liste des mouvements possibles pour la pièce
    
    #Méthode traitant du déplacement de la pièce
    #On récupère la ligne et la colonne de la pièce puis on appel la méthode calc_pos()
    def pieceMove(self, row, col):
        self.row = row
        self.col = col
        self.calcPos()

    #Calcul des coordonnées de la pièce afin de l'afficher à un endroit
    def calcPos(self):
        self.x = self.col * self.square
        self.y = self.row * self.square

    def clearAvailableMoves(self):    #Méthode supprimant la liste des déplacements disponible pour une pièce afin de les re créers
        if len(self.available_moves) > 0:
            self.availableMoves = []   

class Pion(Piece):
    #On appel le constructeur de Piece
    def __init__(self, square, image, cote, type, row, col):
        super().__init__(square, image, color, type, row, col)

    #On clear la liste des déplacement et en fonction du coté du plateau alors on défini les déplacements possibles
    def getAvailableMoves(self, row, col, Board):
        self.clearAvailableMoves()

        if self.cote == Regnant:                            #Si Regnant alors joueur est en bas du plateau
            if row-1 >= 0:                                      #Si le pion peut avancer (pas au bord du plateau) alors :
                if Board[row-1][col-1] == 0:                        #S'il n'y a pas de piece devant le pion
                    self.availableMoves.append((row-1, col))            #Il peut avancer
                else:   #: aussi pour le else ?
                    if piece.cote != self.cote:                     #Sinon, si la piece est une piece ennemie
                        self.availableMoves.append((row-1, col))        #Il peut avancer
       
        if self.cote == Opposant:
            #A remplir