import pygame
from .Board import Board
from .constants import *
from .Joueur import *
from .pieces.Pieces import *
from copy import copy

#Classe qui sert d interface pour le terrain, elle sert a actualiser la position des pieces
# a changer le tour du joueur et a afficher les mouvements possibles

class Game:
    #Une partie prend une largeur, une hauteur, un nombres de colonnes ainsi que de lignes en plus d une fenetre et d un nombres de carreaux
    def __init__(self, Width, Height, Rows, Cols, square, window):
        self.window = window
        self.Board = Board(Width, Height, Rows, Cols, square, window)
        self.square = square
        self.selected = None
        self.turn = Joueur.Regnant
        self.validMoves = []
        self.validPara = []
        self.RegnantPiecesPara = []
        self.OpposantPiecesPara = []

    #Sert a afficher les pieces a leurs nouvel emplacement
    #Est appele a chaques frames (60/s)
    def updateWindow(self):
        self.Board.drawBoard()      #Construit le terrain avec un fond marron et des cases blanches
        self.Board.drawPieces()     #Avec l utilisation de drawPiece permet d actualiser toutes les pieces sur le terrain
        self.Board.drawSide()
        self.drawAvailableMoves()   #Affiche en vert les cases où la piece peut se deplacer
        self.drawPromotion()
        self.drawPara()
        pygame.display.update()     #Actualise l ecran

    def checkGame(self):
        if self.checkmate(self.Board):
            if self.turn == Joueur.Opposant:
                print("Regnant wins")
                return True
            else:
                print("Opposant wins")
                return True

    #On recupere la liste entiere des deplacements possible par l adversaire
    def enemiesMoves(self, piece, Board):
        enemiesMoves = []
        for r in range(len(Board)):
            for c in range (len(Board[r])):
                if Board[r][c] != 0:
                    if Board[r][c].cote != piece.cote:
                        moves = Board[r][c].getAvailableMoves(r, c, Board)
                        for move in moves:
                            enemiesMoves.append(move)
        return enemiesMoves

    #On a deja fait une methode similaire dans piece mais ici on vient la refaire pour plus de faciliter
    def getKingPos(self, Board):
        for r in range(len(Board)):
            for c in range(len(Board[r])):
                if Board[r][c] != 0:
                    if self.turn == Joueur.Regnant:
                        if Board[r][c].type == "Roi" and Board[r][c].cote == self.turn:
                            return (r,c)
                    else:
                        if Board[r][c].type == "GeneralDeJade" and Board[r][c].cote == self.turn:
                            return (r,c)

    #Simule le deplacement d une piece a partir des coordonnees row, col dudit deplacement
    #Peut etre supprime dans le cas d une regle sans verification d echec et mat
    def simulateMove(self, piece, row, col):
        if piece == self.Board.Board[row][col]:
            print("YMCMB")

        print(self.Board.Board[row][col])

        pieceRow, pieceCol = piece.row, piece.col   #On recupere les coordonnees (lignes) de la piece a deplacer
        savePiece = self.Board.Board[row][col]      #On recupere le placement de la piece a l etat "avant deplacement"

        if self.Board.Board[row][col] != 0:
            self.Board.Board[row][col] = 0

        self.Board.Board[piece.row][piece.col], self.Board.Board[row][col] = self.Board.Board[row][col], self.Board.Board[piece.row][piece.col]

        kingPos = self.getKingPos(self.Board.Board)
        if kingPos in self.enemiesMoves(piece, self.Board.Board): #Si le roi est en dange sur sa nouvelle case alors on cancel le move.
            piece.row, piece.col = pieceRow, pieceCol
            self.Board[pieceRow][pieceCol] = piece
            self.Board.Board[row][col] = savePiece
            return False
        else:
            piece.row, piece.col = pieceRow, pieceCol
            self.Board.Board[pieceRow][pieceCol] = piece
            self.Board.Board[pieceRow][pieceCol] = savePiece
            return True

    #Pourquoi faire ? Copie de enemiesMoves mais cette fois de notre cote du terrain et sans le roi ?
    def possibleMoves(self, Board):
        possibleMoves = []
        for r in range(len(Board)):
            for c in range(len(Board[r])):
                if Board[r][c] != 0:
                    if Board[r][c].cote == self.turn and Board[r][c].type != "Roi" or Board[r][c].type != "GeneralDeJade":
                        moves = Board[r][c].getAvailableMoves(r, c, Board)
                        for move in moves:
                            possibleMoves.append(move)
        return possibleMoves

    def checkmate(self, Board):
        kingPos = self.getKingPos(Board.Board)

        if kingPos is not None:
            getKing = Board.getPiece(kingPos[0], kingPos[1])
        
            #On creer un ensemble avec la commande set
            kingAvailableMoves = set(getKing.getAvailableMoves(kingPos[0], kingPos[1], Board.Board))   #On recupere les coups du roi
            enemiesMovesSet = set(self.enemiesMoves(getKing, Board.Board))  #On recupere les coups de l ennemie
            kingMoves = kingAvailableMoves - enemiesMovesSet    #On recupere les coups possible pour le roi 
            set1 = kingAvailableMoves.intersection(enemiesMovesSet) #On recupere les deplacements du roi
            possibleMovesToDef = set1.intersection(self.possibleMoves(Board.Board)) #On recupere les pieces que l on peut utiliser pour proteger le roi (je doute de la fonctionnalite du truc)
            if len(kingMoves) == 0 and len(kingAvailableMoves) != 0 and possibleMovesToDef == 0:
                return True
            else:
                return False
        else:
            return True

    #Reinitialise le placement des pieces sur le plateau
    def reset(self):
        self.Board = Board(self.Board.width, self.Board.height, rows, cols, square, self.window)    #Re creer le plateau a partir des informations dans constantes
        self.selected = None    #reinitialise la valeur de selected
        self.RegnantPiecesLeft, self.OpposantPiecesLeft = 20,20 #Reinitialise le nb de pieces de chaques joueur
        self.validMoves = []    #reinitialise les deplacements disponibles

    #Change le tour du joueur
    def changeTurn(self):
        if self.turn == Joueur.Regnant:
            self.turn = Joueur.Opposant
        else:
            self.turn = Joueur.Regnant

    #Methode privee servant a deplacer une piece dans le jeu appele au cours de self.select()  
    def _move(self, rowVisee, colVisee):
        rowInit, colInit = self.selected.row, self.selected.col
        caseVisee = self.Board.getPiece(rowVisee, colVisee)                       #On vient recuperer la case visee
        if self.selected and (rowVisee, colVisee) in self.validMoves:             #Si la piece qui doit faire le mouvement et la case selectionnee sont dans la liste validMoves (fonctionne)
            if caseVisee == 0 or caseVisee.cote != self.selected.cote:  #Si la case visee pour le mouvement est vide ou correspond a une piece adverse
                #if self.simulateMove(self.selected, row, col):         #Cette methode pose pb pour le deroule du programme, il faut l investiguer

                self.remove(self.Board.Board, self.Board.Board[rowVisee][colVisee], rowVisee, colVisee)
                self.Board.move(self.selected, rowVisee, colVisee)
                self.validMoves = []    #On vide la liste des mouvements

                #Demander a l utilisateur s il veut promouvoir sa piece (Apres un deplacement et donc en entree de zone ou en sortie)
                #Met a true l attribut wasPromotable et donc apres chaques mouvements, propose au joueur de promouvoir
                self.promotionPossible(rowVisee, rowInit)
                if self.selected.isPromotable:
                    self.promotionSelected()

                self.changeTurn()       #On change de tour
                self.selected.isPromotable = False
                self.selected = None    #On enleve la piece de la selectionne
                return True
        return False

    #Methode visant a savoir apres le mouvement du joueur s il veut promouvoir sa piece
    #Si le joueur vient cliquer sur la piece alors elle est promu
    def promotionSelected(self):
        piece = self.selected
        #On doit recuperer les coordonnees du clique afin d identifier si l on clique sur la piece
        #Pour ca on appel la methode getPosition dans Shogi.py et aussi la methode select
        # qui a un if en plus dans le cas de si la piece peu etre promu
        promotionLoop = False
        while promotionLoop == False:           #Tant que le joueur n a pas clique
            for event in pygame.event.get():
                if event.type == pygame.QUIT:   #Si l on quitte le jeu
                    quit()

                if event.type == pygame.MOUSEBUTTONDOWN:                            #Si l utilisateur appuie sur un bouton
                    if pygame.mouse.get_pressed()[0]:                               #Si c est un clique gauche
                        location = pygame.mouse.get_pos()                           #On vient recuperer les coordonnees du clique   #Faudra mettre en place une verification sui le joueur clique en dehors du terrain
                        row, col = self.getPosition(location[0], location[1])       #On vient recuperer la case du clique
                        if piece.row == row and piece.col == col:   #Si l utilisateur clique sur la piece alors
                            #Promotion
                            self.Board.Board[row][col] = piece.promoted()
                            promotionLoop = True
                        else:
                            #Pas de promotion
                            promotionLoop = True

    #Methode visant a savoir si une piece rentre ou sort de la zone de promotion et donc de si elle peut etre promu
    def promotionPossible(self, row, rowInit):
        piece = self.selected
        if piece.type not in pasPromotable:
            if piece.cote == Joueur.Opposant:
                if row <= 2:                        #Si on est ou qu on rentre dans la zone de promotion
                    piece.isPromotable = True
                elif rowInit <= 2:                  #Si on sort de la zone de promotion
                    piece.isPromotable = True
                else:
                    piece.isPromotable = False
            else:                                   #Cote regnant cette fois
                if row >= 6:
                    piece.isPromotable = True
                elif rowInit >= 6:
                    piece.isPromotable = True
                else:
                    piece.isPromotable = False
            self.updateWindow()

    #Methode de debug
    def printBoard(self):
        for row in range(0, len(self.Board.Board)):
            for col in range(0, len(self.Board.Board[row])):
                print(self.Board.Board[row][col])

    #Fonction qui permet, a partir d un clique du joueur, de selectionner la piece sur laquelle le joueur a clique
    #Si le joueur a clique sur une piece, cette piece est alors stockee dans l attribut selected et on affiche ses mouvements
    #Sinon on supprime les mouvements affiches et on change de piece
    def select(self, location):
        row, col = self.getPosition(location[0], location[1])    #On vient recuperer la case du clique
        if self.selected:               #Si on a deja selectionne une piece
            move = self._move(row, col) #Si on clique sur un deplacement possible pour la piece selectionnee, deplace la piece et retourne True
            if not move:                #Si on clique sur une case qui n est pas un deplacement de self.selected
                self.selected = None    #On deselectionne la piece 
                self.select(location)   #On re boucle sur la methode
        else:
            piece = self.Board.getPiece(row, col)
            if piece != 0 and self.turn == piece.cote:
                self.selected = piece
                self.validMoves = piece.getAvailableMoves(row, col, self.Board.Board)
            else:
                self.validMoves = []

    #Supprime une piece du terrain avec comptage de points
    def remove(self, board, piece, row, col):
        if board[row][col] != 0:
            if board[row][col].cote == Joueur.Regnant:
                board[row][col] = 0
                self.OpposantPiecesPara.append(piece.type)
            else:
                board[row][col] = 0
                self.RegnantPiecesPara.append(piece.type)
        print("Piece Regnant :" + str(self.RegnantPiecesPara))
        print("Piece Opposant :" + str(self.OpposantPiecesPara))
        #print("RegnantPiecesLeft : ", self.RegnantPiecesLeft)
        #print("OpposantPiecesLeft : ", self.OpposantPiecesLeft)

    #Affiche en vert les cases où la piece peut se deplacer (utile pour les debutant et le debug)
    def drawAvailableMoves(self):
        if len(self.validMoves) > 0:
            for pos in self.validMoves:
                row, col = pos[0], pos[1]
                pygame.draw.circle(self.window, green, (col*self.square + self.square//2, row*self.square + self.square//2), self.square//8) #Pour bien mettre au centre du carre et pas dans un coin

    #Affiche un rond rouge sur la piece qui peut etre promu
    def drawPromotion(self):
        if self.selected is not None and self.selected.isPromotable == True:
            row, col = self.selected.row, self.selected.col
            pygame.draw.circle(self.window, red, (col*self.square + self.square//2, row*self.square + self.square//2), self.square//8)

    def getPosition(self, x, y):  #Methode servant a convertir la position du clique de la souris en case de clique de la souris
        row = y//square     #Ligne egale a position du clique divise par nb de case du jeu
        col = x//square     # // mais avec les colonnes
        return row, col

    ##Section parachutage

    def selectPara(self, location):
        row, col = self.getPosition(location[0], location[1])
        if self.Board.Side[row][col] != 0:
            pieceSelect = self.Board.getSideType(row, col)

            if self.turn == Joueur.Opposant:
                #Enrichir la classe Joueur, nottament avec le cimetiere
                image = imagesPiecesOpposant
                cimetiere = self.OpposantPiecesPara
            else:
                image = imagesPiecesRegnant
                cimetiere = self.RegnantPiecesPara

            if pieceSelect.type == "Pion":
                if cimetiere.__contains__("Pion") or cimetiere.__contains__("PionDor"):
                    if cimetiere.__contains__("PionDor"):
                        cimetiereRemove = "PionDor"
                    elif cimetiere.__contains__("Pion"):
                        cimetiereRemove = "Pion"

                    piece = Pion(self.square, image["pion"], self.turn, "Pion", 0, 0)
                    self.dropPara(piece, cimetiereRemove)
                else:
                    print("Pas assez de " + str(pieceSelect.type))

            elif pieceSelect.type == "Tour":
                if cimetiere.__contains__("Tour") or cimetiere.__contains__("Dragon"):
                    if cimetiere.__contains__("Dragon"):
                        cimetiereRemove = "Dragon"
                    elif cimetiere.__contains__("Tour"):
                        cimetiereRemove = "Tour"

                    piece = Tour(self.square, image["tour"], self.turn, "Tour", 0, 0)
                    self.dropPara(piece, cimetiereRemove)
                else:
                    print("Pas assez de " + str(pieceSelect.type))

            elif pieceSelect.type == "Fou":
                if cimetiere.__contains__("Fou") or cimetiere.__contains__("ChevalDragon"):
                    if cimetiere.__contains__("ChevalDragon"):
                        cimetiereRemove = "ChevalDragon"
                    elif cimetiere.__contains__("Fou"):
                        cimetiereRemove = "Fou"

                    piece = Fou(self.square, image["fou"], self.turn, "Fou", 0, 0)
                    self.dropPara(piece, cimetiereRemove)
                else:
                    print("Pas assez de " + str(pieceSelect.type))

            elif pieceSelect.type == "GeneralDargent":
                if cimetiere.__contains__("GeneralDargent") or cimetiere.__contains__("ArgentDor"):
                    if cimetiere.__contains__("ArgentDor"):
                        cimetiereRemove = "ArgentDor"
                    elif cimetiere.__contains__("GeneralDargent"):
                        cimetiereRemove = "GeneralDargent"

                    piece = GeneralDargent(self.square, image["generalDargent"], self.turn, "GeneralDargent", 0, 0)
                    self.dropPara(piece, cimetiereRemove)
                else:
                    print("Pas assez de " + str(pieceSelect.type))

            elif pieceSelect.type == "Lancier":
                if cimetiere.__contains__("Lancier") or cimetiere.__contains__("LancierDor"):
                    if cimetiere.__contains__("LancierDor"):
                        cimetiereRemove = "LancierDor"
                    elif cimetiere.__contains__("Lancier"):
                        cimetiereRemove = "Lancier"

                    piece = Lancier(self.square, image["lancier"], self.turn, "Lancier", 0, 0)
                    self.dropPara(piece, cimetiereRemove)
                else:
                    print("Pas assez de " + str(pieceSelect.type))

            elif pieceSelect.type == "Cavalier":
                if cimetiere.__contains__("Cavalier") or cimetiere.__contains__("CavalierDor"):
                    if cimetiere.__contains__("CavalierDor"):
                        cimetiereRemove = "CavalierDor"
                    elif cimetiere.__contains__("Cavalier"):
                        cimetiereRemove = "Cavalier"

                    piece = Cavalier(self.square, image["cavalier"], self.turn, "Cavalier", 0, 0)
                    self.dropPara(piece, cimetiereRemove)
                else:
                    print("Pas assez de " + str(pieceSelect.type))

            elif pieceSelect.type == "GeneralDor":
                if cimetiere.__contains__("GeneralDor"):
                    cimetiereRemove = "GeneralDor"
                    piece = GeneralDor(self.square, image["generalDor"], self.turn, "GeneralDor", 0, 0)
                    self.dropPara(piece, cimetiereRemove)
                else:
                    print("Pas assez de " + str(pieceSelect.type))

    #TODO, separer la methode en 2 comme pour promotion
    def dropPara(self, piece, cimetiereRemove):      #Verifier les regles de parachutage

        pieceFictive = copy(piece)      #Pour ne pas copier la reference
        BoardFictif = copy(self.Board)

        for row in range(0, len(BoardFictif.Board)):
            for col in range(0, len(BoardFictif.Board[row])):
                if BoardFictif.Board[row][col] == 0:   #Pour chacunes des cases vides
                    canBePara = True

                    if piece.type == "Pion":
                        canBePara = self.pionVerifColPara(col, BoardFictif.Board)  #Interdit sur une meme colonne où ce situe un pion (non promu)
                    if canBePara:
                        canBePara = self.pieceDeplacementPara(pieceFictive, row)   #Verif si la piece peut se deplacer de par la creation d un board fictif
                    #TODO Interdit de mettre echec et mat le roi avec un pion
                    if canBePara:
                        self.validPara.append((row, col))

        self.updateWindow()
        
        canBePara2 = True
        while canBePara2 == True:                   #Tant que le joueur n a pas clique
            for event in pygame.event.get():
                if event.type == pygame.QUIT:       #Si l on quitte le jeu
                    quit()

                if event.type == pygame.MOUSEBUTTONDOWN:                            #Si l utilisateur appuie sur un bouton
                    if pygame.mouse.get_pressed()[0]:                               #Si c est un clique gauche
                        location = pygame.mouse.get_pos()                           #On vient recuperer les coordonnees du clique   #Faudra mettre en place une verification sui le joueur clique en dehors du terrain
                        rowClique, colClique = self.getPosition(location[0], location[1])       #On vient recuperer la case du clique
                        if (rowClique, colClique) in self.validPara:
                            #Parachutage
                            piece.row = rowClique
                            piece.col = colClique
                            piece.calcPos()
                            self.Board.Board[rowClique][colClique] = piece
                            print(self.Board.Board[rowClique][colClique])

                            self.validPara = []
                            #Pas forcement le plus jolie mais j ai pas trouve mieux pour le moment
                            if self.turn == Joueur.Opposant:
                                self.OpposantPiecesPara.remove(cimetiereRemove)
                            else:
                                self.RegnantPiecesPara.remove(cimetiereRemove)
                            self.changeTurn()
                            canBePara2 = False
                        else:
                            #Pas de parachutage
                            self.validPara = []
                            canBePara2 = False
        
    def pieceDeplacementPara(self, pieceFictive, row):
        BoardFictif = []
        for i in range(0, rows):
            BoardFictif.append([0 for i in range(3)])  #Pour 9 lignes, creer un tableau a 3 colonnes
        #print(BoardFictif)
        if self.turn == Joueur.Opposant:
            if row < 3:
                BoardFictif[row][1] = pieceFictive  #On place la piece sur la bonne ligne (colonne pas importante donc place au centre)
                moves = BoardFictif[row][1].getAvailableMoves(row, 1, BoardFictif)
                #print(BoardFictif)
                #print(moves)
                if len(moves) == 0:
                    return False
            return True
        else:
            if row > 5:
                BoardFictif[row][1] = pieceFictive  #On place la piece sur la bonne ligne (colonne pas importante)
                moves = BoardFictif[row][1].getAvailableMoves(row, 1, BoardFictif)
                if len(moves) == 0:
                    return False
            return True

    def pionVerifColPara(self, col, BoardFictif):
        for rowi in range (0, len(BoardFictif)):
            if BoardFictif[rowi][col] != 0:                    #Si une piece
                if BoardFictif[rowi][col].cote == self.turn:   #Si de la meme equipe
                    if BoardFictif[rowi][col].type == "Pion":  #Si c est un Pion (non promu)
                        return False
        return True

    def drawPara(self):
        if len(self.validPara) > 0:
            for pos in self.validPara:
                row, col = pos[0], pos[1]
                pygame.draw.circle(self.window, cyan, (col*self.square + self.square//2, row*self.square + self.square//2), self.square//8) #Pour bien mettre au centre du carre et pas dans un coin
