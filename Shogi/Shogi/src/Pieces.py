import pygame

from .constants import *

class Piece:    #On cr�er une classe Piece
    def __init__(self, square, image, cote, type, row, col):   #Constructeur prenant
        self.square = square    #Dimension ?
        self.image = image      #Image de la piece
        self.cote = cote        #Si le joueur a un roi ou un g�n�ral de jade    (Regnant ou Opposant)
        self.row = row          #Position ligne ?
        self.col = col          #Position colonne ?
        self.type = type        #Type (roi, cavalier ...)
        self.x = 0              #Je ne sais pas
        self.y = 0              #Idem
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

class Pion(Piece):
    #On appel le constructeur de Piece
    def __init__(self, square, image, cote, type, row, col):
        super().__init__(square, image, color, type, row, col)

    #On clear la liste des d�placement et en fonction du cot� du plateau alors on d�fini les d�placements possibles
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