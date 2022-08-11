from Pieces import *

#Classe Pion h�rite de la classe Piece
class Pion(Pieces):  

    #On appel le constructeur de Piece
    ###Rajouter pionMouvement dans le constructeur ?
    def __init__(self, square, image, cote, type, row, col):
        super().__init__(square, image, cote, type, row, col)

    #M�thode concernant la liste des mouvements possibles pour la pi�ce (ici le pion)
    #On vient r�initialiser les mouvements de la pi�ce en question � son acquisition
    #Puis en fonction du cot� du terrain (Regnant ou Opposant) alors on d�finit son sens de d�placement
    ###La m�thode peut compl�tement �tre simplifi� (pour plus tard)
    def getAvailableMoves(self, row, col, Board):
        self.clearAvailableMoves()

        pionMouvement = 0;

        if self.cote == Joueur.Regnant:                            #Si Regnant alors joueur est en bas du plateau

            pionMouvement = -1

            if row + pionMouvement >= 0:                                      #Si le pion peut avancer (pas au bord du plateau) alors :
                if Board[row + pionMouvement][col] == 0:                          #S'il n'y a pas de piece devant le pion
                    self.availableMoves.append((row + pionMouvement, col))            #Il peut avancer
                else:
                    piece = Board[row + pionMouvement][col]
                    if piece.cote != self.cote:                     #Sinon, si la piece est une piece ennemie
                        self.availableMoves.append((row + pionMouvement, col))        #Il peut avancer
       
        if self.cote == Joueur.Opposant:                           #Si Opposant alors en haut du plateau

            pionMouvement = 1

            if row + pionMouvement < len(Board):                                     
                if Board[row + pionMouvement][col] == 0:                        
                    self.availableMoves.append((row + pionMouvement, col))            
                else:
                    piece = Board[row + pionMouvement][col]
                    if piece.cote != self.cote:                    
                        self.availableMoves.append((row + pionMouvement, col))

        return self.availableMoves