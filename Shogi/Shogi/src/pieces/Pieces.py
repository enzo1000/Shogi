import pygame

from ..constants import *

class Pieces:    #On créer une classe Piece
    def __init__(self, square, image, cote, type, row, col):   #Constructeur prenant
        self.square = square    #Dimension ?
        self.image = image      #Image de la piece
        self.cote = cote        #Si le joueur a un roi ou un général de jade    (Regnant ou Opposant)
        self.row = row          #Position ligne ?
        self.col = col          #Position colonne ?
        self.type = type        #Type (roi, cavalier ...)
        self.x = 0              #Position en colonnes pour x * square (la taille d'un carré) pour avoir les coordonnées de la piece sur le terrain
        self.y = 0              #Idem mais pour les lignes
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