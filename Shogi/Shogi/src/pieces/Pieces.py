import pygame

from ..constants import *

class Pieces:    #On cr�er une classe Piece
    def __init__(self, square, image, cote, type, row, col):   #Constructeur prenant
        self.square = square    #Dimension ?
        self.image = image      #Image de la piece
        self.cote = cote        #Si le joueur a un roi ou un g�n�ral de jade    (Regnant ou Opposant)
        self.row = row          #Position ligne ?
        self.col = col          #Position colonne ?
        self.type = type        #Type (roi, cavalier ...)
        self.x = 0              #Position en colonnes pour x * square (la taille d'un carr�) pour avoir les coordonn�es de la piece sur le terrain
        self.y = 0              #Idem mais pour les lignes
        self.availableMoves = []   #Liste des mouvements possibles pour la pi�ce
    
    #M�thode traitant du d�placement de la pi�ce
    #On r�cup�re la ligne et la colonne de la pi�ce puis on appel la m�thode calc_pos()
    def pieceMove(self, row, col):
        self.row = row
        self.col = col
        self.calcPos()

    #Calcul des coordonn�es de la pi�ce afin de l'afficher � un endroit
    def calcPos(self):
        self.x = self.col * self.square
        self.y = self.row * self.square

    def clearAvailableMoves(self):    #M�thode supprimant la liste des d�placements disponible pour une pi�ce afin de les re cr�ers
        if len(self.available_moves) > 0:
            self.availableMoves = []   