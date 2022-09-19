from ..Joueur import *
from ..constants import *
from ..pieces import *

#Je me rend compte lors du test du programme qu'il n'est pas possible de faire de l'héritage en python
# dans différents fichiers tel que le java par exemple.
#Je garde alors les fichiers séparés mais rajoute leurs contenu au sein du fichier Pieces.py

class Pieces:    #On créer une classe Pieces
    def __init__(self, square, image, cote, type, row, col):   #Constructeur prenant
        self.square = square        #Dimension ?
        self.image = image          #Image de la piece
        self.cote = cote            #Si le joueur a un roi ou un général de jade    (Regnant ou Opposant)
        self.row = row              #Position ligne ?
        self.col = col              #Position colonne ?
        self.type = type            #Type (roi, cavalier ...)
        self.x = 0                  #Position en colonnes pour x * square (la taille d'un carré) pour avoir les coordonnées de la piece sur le terrain
        self.y = 0                  #Idem mais pour les lignes
        self.availableMoves = []    #Liste des mouvements possibles pour la pièce
        self.calcPos()
        self.isPromotable = False
    
    #Méthode traitant du déplacement de la pièce
    #On récupère la ligne et la colonne de la pièce puis on appel la méthode calc_pos()
    ##Fonctionnel
    def pieceMove(self, row, col):
        #print(str(row) + str(col) + " | " + str(self.row) + str(self.col))
        self.row = row
        self.col = col
        self.calcPos()

    #Calcul des coordonnées de la pièce afin de l'afficher à un endroit 
    ##Fonctionnel
    def calcPos(self):
        self.x = self.col * self.square
        self.y = self.row * self.square

    def clearAvailableMoves(self):    #Méthode supprimant la liste des déplacements disponible pour une pièce afin de les re créers
        if len(self.availableMoves) > 0:
            self.availableMoves = []

    def __str__(self):
        return "" + self.type + " | pos : " + str(self.row) + ", " + str(self.col)

#### Pieces ####

class Lancier(Pieces):
    def __init__(self, square, image, cote, type, row, col):
        super().__init__(square, image, cote, type, row, col)

    def getAvailableMoves(self, row, col, Board):
        self.clearAvailableMoves()

        if self.cote == Joueur.Regnant:             #Si Regnant alors joueur est en bas du plateau
            for j in range(row+1, len(Board)):      #Vers le haut du plateau

                if Board[j][col] == 0:              #Si pas de piece
                    self.availableMoves.append((j, col))
                elif Board[j][col].cote != self.cote:
                    self.availableMoves.append((j, col))
                    break
                else:
                    break
            
        if self.cote == Joueur.Opposant:
            for i in range(row-1, -1, -1): #Vers le bas jusqu'au bors du tableau

                if Board[i][col] != 0:
                    if Board[i][col].cote != self.cote:
                        self.availableMoves.append((i, col))
                        break
                    else:
                        break
                self.availableMoves.append((i, col))
        return self.availableMoves

    def promoted(self):
        if self.cote == Joueur.Opposant:
            return LancierDor(self.square, imagesPromotionsOpposant["lancierDor"], Joueur.Opposant, "LancierDor", self.row, self.col)
        else:
            return LancierDor(self.square, imagesPromotionsRegnant["lancierDor"], Joueur.Regnant, "LancierDor", self.row, self.col)

class Cavalier(Pieces):
    def __init__(self, square, image, cote, type, row, col):
        super().__init__(square, image, cote, type, row, col)

    def getAvailableMoves(self, row, col, Board):
        self.clearAvailableMoves()

        if self.cote == Joueur.Regnant:            #Si Regnant alors joueur est en bas du plateau
            if row + 2 < len(Board[row]) and col + 1 < len(Board):
                if Board[row+2][col+1] == 0 or Board[row+2][col+1].cote != self.cote:
                    self.availableMoves.append((row+2, col+1))

            if row + 2 < len(Board[row]) and col - 1 >= 0:
                if Board[row+2][col-1] == 0 or Board[row+2][col-1].cote != self.cote:
                    self.availableMoves.append((row+2, col-1))

        if self.cote == Joueur.Opposant:   
            if row - 2 >= 0 and col + 1 < len(Board):
                if Board[row-2][col+1] == 0 or Board[row-2][col+1].cote != self.cote:
                    self.availableMoves.append((row-2, col+1))

            if row - 2 >= 0 and col - 1 >= 0:
                if Board[row-2][col-1] == 0 or Board[row-2][col-1].cote != self.cote:
                    self.availableMoves.append((row-2, col-1))
        return self.availableMoves

    def promoted(self):
        if self.cote == Joueur.Opposant:
            return CavalierDor(self.square, imagesPromotionsOpposant["cavalierDor"], Joueur.Opposant, "CavalierDor", self.row, self.col)
        else:
            return CavalierDor(self.square, imagesPromotionsRegnant["cavalierDor"], Joueur.Regnant, "CavalierDor", self.row, self.col)

class GeneralDargent(Pieces):
    def __init__(self, square, image, cote, type, row, col):
        super().__init__(square, image, cote, type, row, col)

    def generalLigneHautBas(self, rowi, Board):
         for coli in [self.col-1, self.col, self.col+1]:     #On fait la ligne du haut en premier (les 3 cases en haut de la piece)
            if rowi >= 0 and rowi < len(Board):
                if coli >= 0 and coli < len(Board[rowi]):
                    if coli != self.col or rowi != self.row:
                        if Board[rowi][coli] == 0:
                            self.availableMoves.append((rowi, coli))
                        elif Board[rowi][coli].cote != self.cote:
                            self.availableMoves.append((rowi, coli))

    def getAvailableMoves(self, row, col, Board):
        self.clearAvailableMoves()

        if self.cote == Joueur.Opposant:
            self.generalLigneHautBas(row - 1, Board)
            if row + 1 in range(0, len(Board)) and col + 1 in range(0, len(Board[row])):
                if Board[row + 1][col + 1] == 0:
                    self.availableMoves.append((row + 1, col + 1))
                elif Board[row + 1][col + 1].cote != self.cote:
                    self.availableMoves.append((row + 1, col + 1))

            if row + 1 in range(0, len(Board)) and col - 1 in range(0, len(Board[row])):
                if Board[row + 1][col - 1] == 0:
                    self.availableMoves.append((row + 1, col - 1))
                elif Board[row + 1][col - 1].cote != self.cote:
                    self.availableMoves.append((row + 1, col - 1))

        else:
            self.generalLigneHautBas(row + 1, Board)
            if row - 1 in range(0, len(Board)) and col + 1 in range(0, len(Board[row])):
                if Board[row - 1][col + 1] == 0:
                    self.availableMoves.append((row - 1, col + 1))
                elif Board[row - 1][col + 1].cote != self.cote:
                    self.availableMoves.append((row - 1, col + 1))

            if row - 1 in range(0, len(Board)) and col - 1 in range(0, len(Board[row])):
                if Board[row - 1][col - 1] == 0:
                    self.availableMoves.append((row - 1, col - 1))
                elif Board[row - 1][col - 1].cote != self.cote:
                    self.availableMoves.append((row - 1, col - 1))
        return self.availableMoves

    def promoted(self):
        if self.cote == Joueur.Opposant:
            return ArgentDor(self.square, imagesPromotionsOpposant["argentDor"], Joueur.Opposant, "ArgentDor", self.row, self.col)
        else:
            return ArgentDor(self.square, imagesPromotionsRegnant["argentDor"], Joueur.Regnant, "ArgentDor", self.row, self.col)

class GeneralDor(Pieces):
    def __init__(self, square, image, cote, type, row, col):
        super().__init__(square, image, cote, type, row, col)

    def generalLigneHautBas(self, rowi, Board):
         for coli in [self.col-1, self.col, self.col+1]:     #On fait la ligne du haut en premier (les 3 cases en haut de la piece)
             if rowi >= 0 and rowi < len(Board):
                if coli >= 0 and coli < len(Board[rowi]):
                     if coli != self.col or rowi != self.row:
                        if Board[rowi][coli] == 0:
                            self.availableMoves.append((rowi, coli))
                        elif Board[rowi][coli].cote != self.cote:
                            self.availableMoves.append((rowi, coli))

    def getAvailableMoves(self, row, col, Board):
        self.clearAvailableMoves()

        if self.cote == Joueur.Opposant:
            self.generalLigneHautBas(row - 1, Board)
            self.generalLigneHautBas(row, Board)
            if row + 1 in range(0, len(Board)):
                if Board[row + 1][col] == 0:
                    self.availableMoves.append((row + 1, col))
                elif Board[row + 1][col].cote != self.cote:
                    self.availableMoves.append((row + 1, col))
        else:
            self.generalLigneHautBas(row + 1, Board)
            self.generalLigneHautBas(row, Board)
            if Board[row - 1][col] == 0:
                self.availableMoves.append((row - 1, col))
            elif Board[row - 1][col].cote != self.cote:
                self.availableMoves.append((row - 1, col))
        return self.availableMoves

class Roi(Pieces):
    def __init__(self, square, image, cote, type, row, col):
        super().__init__(square, image, cote, type, row, col)

    #Fonction qui pour une ligne donnée, donne les mouvements possibles en parcourant les 3 cases en face de ladite piece
    #Pour expliquer plus simplement, le roi il peut aller partout case par case, avec cette fonction, on simplifie en mémoire le calcul des mouvements
    # pour la ligne en haut du roi, celle du milieu (en supprimant la case du roi) et en bas du roi
    def kingLigneHautBas(self, rowi, Board):
        for coli in [self.col-1, self.col, self.col+1]:     #On fait la ligne du haut en premier (les 3 cases en haut de la piece)
            if rowi >= 0 and rowi < len(Board):
                if coli >= 0 and coli < len(Board[rowi]):
                    if coli != self.col or rowi != self.row:        #Pour éviter de pouvoir faire bouger le roi sur lui même (sur place)
                        if Board[rowi][coli] == 0:
                            self.availableMoves.append((rowi, coli))
                        elif Board[rowi][coli].cote != self.cote:
                            self.availableMoves.append((rowi, coli))
        
    def getAvailableMoves(self, row, col, Board):
        self.clearAvailableMoves()

        self.kingLigneHautBas(row - 1, Board)
        self.kingLigneHautBas(row, Board)
        self.kingLigneHautBas(row + 1, Board)
        return self.availableMoves

class Tour(Pieces):
    def __init__(self, square, image, cote, type, row, col):
        super().__init__(square, image, cote, type, row, col)

    def getAvailableMoves(self, row, col, Board):
        self.clearAvailableMoves()

        for i in range(row+1, len(Board)): #Vers le bas jusqu'au bors du tableau

            if Board[i][col] == 0:
                self.availableMoves.append((i, col))

            elif Board[i][col].cote != self.cote:
                self.availableMoves.append((i, col))
                break
            else:
                break

        for j in range(row-1, -1, -1):  #On va de row-1 à -1 avec un pas de -1 par -1 (-1 exclue) vers le haut

            if Board[j][col] == 0:
                self.availableMoves.append((j, col))

            elif Board[j][col].cote != self.cote:
                self.availableMoves.append((j, col))
                break
            else:
                break

        for k in range(col+1, len(Board[row])): #On va vers la droite

            if Board[row][k] == 0:
                self.availableMoves.append((row, k))

            elif Board[row][k].cote != self.cote:
                self.availableMoves.append((row, k))
                break
            else:
                break

        for l in range(col-1, -1, -1):  #On va de col-1 à -1 avec un pas de -1 par -1 (-1 exclue) vers la gauche

            if Board[row][l] == 0:
                self.availableMoves.append((row, l))

            elif Board[row][l].cote != self.cote:
                self.availableMoves.append((row, l))
                break
            else:
                break

        return self.availableMoves

    def promoted(self):
        if self.cote == Joueur.Opposant:
            return Dragon(self.square, imagesPromotionsOpposant["dragon"], Joueur.Opposant, "Dragon", self.row, self.col)
        else:
            return Dragon(self.square, imagesPromotionsRegnant["dragon"], Joueur.Regnant, "Dragon", self.row, self.col)

class Fou(Pieces):
    
    def __init__(self, square, image, cote, type, row, col):
        super().__init__(square, image, cote, type, row, col)

    def getAvailableMoves(self, row, col, Board):
        self.clearAvailableMoves()

        rowi = row + 1  #Cette fois le mec de la vidéo préfère passer par d'autres variables
        coli = col + 1  #C'est pas une mauvaise idée mais c'est pas nécessaire non plus, bref

        while rowi < len(Board) and coli < len(Board[row]):
            if Board[rowi][coli] == 0:
                self.availableMoves.append((rowi, coli))
                rowi += 1
                coli += 1

            else:
                if Board[rowi][coli].cote != self.cote:
                    self.availableMoves.append((rowi, coli))
                    break
                break

        rowi = row - 1
        coli = col - 1

        while rowi >= 0 and coli >= 0:
            if Board[rowi][coli] == 0:
                self.availableMoves.append((rowi, coli))
                rowi -= 1
                coli -= 1
            
            else:
                if Board[rowi][coli].cote != self.cote:
                    self.availableMoves.append((rowi, coli))
                    break
                break

        rowi = row + 1
        coli = col - 1

        while rowi < len(Board) and coli >= 0:
            if Board[rowi][coli] == 0:
                self.availableMoves.append((rowi, coli))
                rowi += 1
                coli -= 1

            else:
                if Board[rowi][coli].cote != self.cote:
                    self.availableMoves.append((rowi, coli))
                    break
                break

        rowi = row - 1
        coli = col + 1

        while rowi >= 0 and coli < len(Board[row]):
            if Board[rowi][coli] == 0:
                self.availableMoves.append((rowi, coli))
                rowi -= 1
                coli += 1

            else:
                if Board[rowi][coli].cote != self.cote:
                    self.availableMoves.append((rowi, coli))
                    break
                break
        return self.availableMoves

    def promoted(self):
        if self.cote == Joueur.Opposant:
            return ChevalDragon(self.square, imagesPromotionsOpposant["chevalDragon"], Joueur.Opposant, "ChevalDragon", self.row, self.col)
        else:
            return ChevalDragon(self.square, imagesPromotionsRegnant["chevalDragon"], Joueur.Regnant, "ChevalDragon", self.row, self.col)

#Classe Pion hérite de la classe Piece
class Pion(Pieces):  

    #On appel le constructeur de Piece
    ###Rajouter pionMouvement dans le constructeur ?
    def __init__(self, square, image, cote, type, row, col):
        super().__init__(square, image, cote, type, row, col)

    #Méthode concernant la liste des mouvements possibles pour la pièce (ici le pion)
    #On vient réinitialiser les mouvements de la pièce en question à son acquisition
    #Puis en fonction du coté du terrain (Regnant ou Opposant) alors on définit son sens de déplacement
    ###La méthode peut complétement être simplifié (pour plus tard)
    def getAvailableMoves(self, row, col, Board):
        self.clearAvailableMoves()

        if self.cote == Joueur.Regnant:                            #Si Regnant alors joueur est en haut du plateau
            pionMouvement = 1
            if row + pionMouvement < len(Board):                                      #Si le pion peut avancer (pas au bord du plateau) alors :
                if Board[row + pionMouvement][col] == 0:                              #S'il n'y a pas de piece devant le pion
                    self.availableMoves.append((row + pionMouvement, col))            #Il peut avancer
                else:
                    piece = Board[row + pionMouvement][col]
                    if piece.cote != self.cote:                     #Sinon, si la piece est une piece ennemie
                        self.availableMoves.append((row + pionMouvement, col))        #Il peut avancer
       
        if self.cote == Joueur.Opposant:                            #Si Opposant alors en bas du plateau
            pionMouvement = -1
            if row + pionMouvement >= 0:
                if Board[row + pionMouvement][col] == 0:
                    self.availableMoves.append((row + pionMouvement, col))
                else:
                    piece = Board[row + pionMouvement][col]
                    if piece.cote != self.cote:                    
                        self.availableMoves.append((row + pionMouvement, col))
        return self.availableMoves

    def promoted(self):
        if self.cote == Joueur.Opposant:
            return PionDor(self.square, imagesPromotionsOpposant["pionDor"], Joueur.Opposant, "PionDor", self.row, self.col)
        else:
            return PionDor(self.square, imagesPromotionsRegnant["pionDor"], Joueur.Regnant, "PionDor", self.row, self.col)

class GeneralDeJade(Roi):
    def __init__(self, square, image, cote, type, row, col):
        super().__init__(square, image, cote, type, row, col)

    def getAvailableMoves(self, row, col, Board):
        return super().getAvailableMoves(row, col, Board)

#### Pieces Promu ####

class LancierDor(GeneralDor):
    def __init__(self, square, image, cote, type, row, col):
        super().__init__(square, image, cote, type, row, col)

    def getAvailableMoves(self, row, col, Board):
        return super().getAvailableMoves(row, col, Board)

class CavalierDor(GeneralDor):
    def __init__(self, square, image, cote, type, row, col):
        super().__init__(square, image, cote, type, row, col)

    def getAvailableMoves(self, row, col, Board):
        return super().getAvailableMoves(row, col, Board)

class ArgentDor(GeneralDor):
    def __init__(self, square, image, cote, type, row, col):
        super().__init__(square, image, cote, type, row, col)

    def getAvailableMoves(self, row, col, Board):
        return super().getAvailableMoves(row, col, Board)

class PionDor(GeneralDor):
    def __init__(self, square, image, cote, type, row, col):
        super().__init__(square, image, cote, type, row, col)

    def getAvailableMoves(self, row, col, Board):
        return super().getAvailableMoves(row, col, Board)

class Dragon(Pieces):
    def __init__(self, square, image, cote, type, row, col):
        super().__init__(square, image, cote, type, row, col)

    def kingLigneHautBas(self, rowi, Board):
        for coli in [self.col-1, self.col, self.col+1]:     #On fait la ligne du haut en premier (les 3 cases en haut de la piece)
            if rowi >= 0 and rowi < len(Board):
                if coli >= 0 and coli < len(Board[rowi]):
                    if coli != self.col or rowi != self.row:        #Pour éviter de pouvoir faire bouger le roi sur lui même (sur place)
                        if Board[rowi][coli] == 0:
                            self.availableMoves.append((rowi, coli))
                        elif Board[rowi][coli].cote != self.cote:
                            self.availableMoves.append((rowi, coli))
        
    def getAvailableMoves(self, row, col, Board):
        self.clearAvailableMoves()

        self.kingLigneHautBas(row - 1, Board)
        self.kingLigneHautBas(row, Board)
        self.kingLigneHautBas(row + 1, Board)

        for i in range(row+1, len(Board)): #Vers le bas jusqu'au bors du tableau

            if Board[i][col] == 0:
                self.availableMoves.append((i, col))

            elif Board[i][col].cote != self.cote:
                self.availableMoves.append((i, col))
                break
            else:
                break

        for j in range(row-1, -1, -1):  #On va de row-1 à -1 avec un pas de -1 par -1 (-1 exclue) vers le haut

            if Board[j][col] == 0:
                self.availableMoves.append((j, col))

            elif Board[j][col].cote != self.cote:
                self.availableMoves.append((j, col))
                break
            else:
                break

        for k in range(col+1, len(Board[row])): #On va vers la droite

            if Board[row][k] == 0:
                self.availableMoves.append((row, k))

            elif Board[row][k].cote != self.cote:
                self.availableMoves.append((row, k))
                break
            else:
                break

        for l in range(col-1, -1, -1):  #On va de col-1 à -1 avec un pas de -1 par -1 (-1 exclue) vers la gauche

            if Board[row][l] == 0:
                self.availableMoves.append((row, l))

            elif Board[row][l].cote != self.cote:
                self.availableMoves.append((row, l))
                break
            else:
                break
        return self.availableMoves


class ChevalDragon(Pieces):
    def __init__(self, square, image, cote, type, row, col):
        super().__init__(square, image, cote, type, row, col)

    def kingLigneHautBas(self, rowi, Board):
        for coli in [self.col-1, self.col, self.col+1]:     #On fait la ligne du haut en premier (les 3 cases en haut de la piece)
            if rowi >= 0 and rowi < len(Board):
                if coli >= 0 and coli < len(Board[rowi]):
                    if coli != self.col or rowi != self.row:        #Pour éviter de pouvoir faire bouger le roi sur lui même (sur place)
                        if Board[rowi][coli] == 0:
                            self.availableMoves.append((rowi, coli))
                        elif Board[rowi][coli].cote != self.cote:
                            self.availableMoves.append((rowi, coli))
        
    def getAvailableMoves(self, row, col, Board):
        self.clearAvailableMoves()

        self.kingLigneHautBas(row - 1, Board)
        self.kingLigneHautBas(row, Board)
        self.kingLigneHautBas(row + 1, Board)

        rowi = row + 1  #Cette fois le mec de la vidéo préfère passer par d'autres variables
        coli = col + 1  #C'est pas une mauvaise idée mais c'est pas nécessaire non plus, bref

        while rowi < len(Board) and coli < len(Board[row]):
            if Board[rowi][coli] == 0:
                self.availableMoves.append((rowi, coli))
                rowi += 1
                coli += 1

            else:
                if Board[rowi][coli].cote != self.cote:
                    self.availableMoves.append((rowi, coli))
                    break
                break

        rowi = row - 1
        coli = col - 1

        while rowi >= 0 and coli >= 0:
            if Board[rowi][coli] == 0:
                self.availableMoves.append((rowi, coli))
                rowi -= 1
                coli -= 1
            
            else:
                if Board[rowi][coli].cote != self.cote:
                    self.availableMoves.append((rowi, coli))
                    break
                break

        rowi = row + 1
        coli = col - 1

        while rowi < len(Board) and coli >= 0:
            if Board[rowi][coli] == 0:
                self.availableMoves.append((rowi, coli))
                rowi += 1
                coli -= 1

            else:
                if Board[rowi][coli].cote != self.cote:
                    self.availableMoves.append((rowi, coli))
                    break
                break

        rowi = row - 1
        coli = col + 1

        while rowi >= 0 and coli < len(Board[row]):
            if Board[rowi][coli] == 0:
                self.availableMoves.append((rowi, coli))
                rowi -= 1
                coli += 1

            else:
                if Board[rowi][coli].cote != self.cote:
                    self.availableMoves.append((rowi, coli))
                    break
                break
        return self.availableMoves