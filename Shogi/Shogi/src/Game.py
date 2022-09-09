import pygame
from .Board import Board
from .constants import *
from .Joueur import *
from .pieces.Pieces import *

#Classe qui sert d'interface pour le terrain, elle sert � actualiser la position des pi�ces
# � changer le tour du joueur et � afficher les mouvements possibles

class Game:
    #Une partie prend une largeur, une hauteur, un nombres de colonnes ainsi que de lignes en plus d'une fen�tre et d'un nombres de carreaux
    def __init__(self, Width, Height, Rows, Cols, square, window):
        self.window = window
        self.Board = Board(Width, Height, Rows, Cols, square, window)
        self.square = square
        self.selected = None
        self.turn = Joueur.Regnant
        self.validMoves = []
        self.RegnantPiecesLeft = 20
        self.OpposantPiecesLeft = 20

    #Sert � afficher les pi�ces � leurs nouvel emplacement
    #Est appel� � chaques frames (60/s)
    def updateWindow(self):
        self.Board.drawBoard()      #Construit le terrain avec un fond marron et des cases blanches
        self.Board.drawPieces()     #Avec l'utilisation de drawPiece permet d'actualiser toutes les pi�ces sur le terrain
        self.drawAvailableMoves()   #Affiche en vert les cases o� la pi�ce peut se d�placer
        self.drawPromotion()
        pygame.display.update()     #Actualise l'�cran

    def checkGame(self):
        if self.checkmate(self.Board):
            if self.turn == Joueur.Opposant:
                print("Regnant wins")
                return True
            else:
                print("Opposant wins")
                return True

    #On r�cup�re la liste enti�re des d�placements possible par l'adversaire
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

    #On a d�j� fait une m�thode similaire dans pi�ce mais ici on vient la refaire pour plus de faciliter
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

    #Simule le d�placement d'une pi�ce � partir des coordonn�es row, col dudit d�placement
    #Peut �tre supprim� dans le cas d'une r�gle sans v�rification d'�chec et mat
    def simulateMove(self, piece, row, col):
        if piece == self.Board.Board[row][col]:
            print("YMCMB")

        print(self.Board.Board[row][col])

        pieceRow, pieceCol = piece.row, piece.col   #On r�cup�re les coordonn�es (lignes) de la pi�ce � d�placer
        savePiece = self.Board.Board[row][col]      #On r�cup�re le placement de la pi�ce � l'�tat "avant d�placement"

        if self.Board.Board[row][col] != 0:
            self.Board.Board[row][col] = 0

        self.Board.Board[piece.row][piece.col], self.Board.Board[row][col] = self.Board.Board[row][col], self.Board.Board[piece.row][piece.col]

        kingPos = self.getKingPos(self.Board.Board)
        if kingPos in self.enemiesMoves(piece, self.Board.Board): #Si le roi est en dang� sur sa nouvelle case alors on cancel le move.
            piece.row, piece.col = pieceRow, pieceCol
            self.Board[pieceRow][pieceCol] = piece
            self.Board.Board[row][col] = savePiece
            return False
        else:
            piece.row, piece.col = pieceRow, pieceCol
            self.Board.Board[pieceRow][pieceCol] = piece
            self.Board.Board[pieceRow][pieceCol] = savePiece
            return True

    #Pourquoi faire ? Copie de enemiesMoves mais cette fois de notre cot� du terrain et sans le roi ?
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
        
            #On cr�er un ensemble avec la commande set
            kingAvailableMoves = set(getKing.getAvailableMoves(kingPos[0], kingPos[1], Board.Board))   #On r�cup�re les coups du roi
            enemiesMovesSet = set(self.enemiesMoves(getKing, Board.Board))  #On r�cup�re les coups de l'ennemie
            kingMoves = kingAvailableMoves - enemiesMovesSet    #On r�cup�re les coups possible pour le roi 
            set1 = kingAvailableMoves.intersection(enemiesMovesSet) #On r�cup�re les d�placements du roi
            possibleMovesToDef = set1.intersection(self.possibleMoves(Board.Board)) #On r�cup�re les pi�ces que l'on peut utiliser pour prot�ger le roi (je doute de la fonctionnalit� du truc)
            if len(kingMoves) == 0 and len(kingAvailableMoves) != 0 and possibleMovesToDef == 0:
                return True
            else:
                return False

        else:
            return True

    #R�initialise le placement des pi�ces sur le plateau
    def reset(self):
        self.Board = Board(widthS, heightS, rows, cols, square, self.window)    #Re cr�er le plateau � partir des informations dans constantes
        self.selected = None    #r�initialise la valeur de selected
        self.RegnantPiecesLeft, self.OpposantPiecesLeft = 20,20 #R�initialise le nb de pi�ces de chaques joueur
        self.validMoves = []    #r�initialise les d�placements disponibles

    #Change le tour du joueur
    def changeTurn(self):
        if self.turn == Joueur.Regnant:
            self.turn = Joueur.Opposant
        else:
            self.turn = Joueur.Regnant

    #M�thode priv�e servant � d�placer une pi�ce dans le jeu appel� au cours de self.select()  
    def _move(self, rowVisee, colVisee):
        rowInit, colInit = self.selected.row, self.selected.col
        caseVisee = self.Board.getPiece(rowVisee, colVisee)                       #On vient r�cup�rer la case vis�e
        if self.selected and (rowVisee, colVisee) in self.validMoves:             #Si la piece qui doit faire le mouvement et la case s�lectionn�e sont dans la liste validMoves (fonctionne)
            if caseVisee == 0 or caseVisee.cote != self.selected.cote:  #Si la case vis�e pour le mouvement est vide ou correspond � une pi�ce adverse
                #if self.simulateMove(self.selected, row, col):         #Cette m�thode pose pb pour le d�roul� du programme, il faut l'investiguer

                self.remove(self.Board.Board, self.selected, rowVisee, colVisee)
                self.Board.move(self.selected, rowVisee, colVisee)
                self.validMoves = []    #On vide la liste des mouvements

                #Demander � l'utilisateur s'il veut promouvoir sa pi�ce (Apr�s un d�placement et donc en entr�e de zone ou en sortie)
                #Met � true l'attribut wasPromotable et donc apr�s chaques mouvements, propose au joueur de promouvoir
                self.promotionPossible(rowVisee, rowInit)
                if self.selected.isPromotable:
                    self.promotionSelected()

                self.changeTurn()       #On change de tour
                self.selected.isPromotable = False
                self.selected = None    #On enl�ve la pi�ce de la s�lectionne
                return True
        return False

    #M�thode visant � savoir apr�s le mouvement du joueur s'il veut promouvoir sa pi�ce
    #Si le joueur vient cliquer sur la pi�ce alors elle est promu
    def promotionSelected(self):
        piece = self.selected
        #On doit r�cup�rer les coordonn�es du clique afin d'identifier si l'on clique sur la pi�ce
        #Pour �a on appel la m�thode getPosition dans Shogi.py et aussi la m�thode select
        # qui a un if en plus dans le cas de si la pi�ce peu �tre promu
        promotionLoop = False
        while promotionLoop == False:           #Tant que le joueur n'a pas cliqu�
            for event in pygame.event.get():
                if event.type == pygame.QUIT:   #Si l'on quitte le jeu
                    run = False
                    quit()

                if event.type == pygame.MOUSEBUTTONDOWN:                            #Si l'utilisateur appuie sur un bouton
                    if pygame.mouse.get_pressed()[0]:                               #Si c'est un clique gauche
                        location = pygame.mouse.get_pos()                           #On vient r�cup�rer les coordonn�es du clique   #Faudra mettre en place une v�rification sui le joueur clique en dehors du terrain
                        row, col = self.getPosition(location[0], location[1])       #On vient r�cup�rer la case du clique
                        if piece.row == row and piece.col == col:   #Si l'utilisateur clique sur la pi�ce alors
                            #Promotion
                            self.Board.Board[row][col] = piece.promoted()
                            promotionLoop = True
                        else:
                            #Pas de promotion
                            promotionLoop = True

    #M�thode visant � savoir si une pi�ce rentre ou sort de la zone de promotion et donc de si elle peut �tre promu
    def promotionPossible(self, row, rowInit):
        piece = self.selected
        if piece.type not in pasPromotable:
            if piece.cote == Joueur.Opposant:
                if row <= 2:                        #Si on est ou qu'on rentre dans la zone de promotion
                    piece.isPromotable = True
                elif rowInit <= 2:                  #Si on sort de la zone de promotion
                    piece.isPromotable = True
                else: 
                    piece.isPromotable = False
            else:                                   #Cot� regnant cette fois
                if row >= 6:                       
                    piece.isPromotable = True
                elif rowInit >= 6:                  
                    piece.isPromotable = True
                else:
                    piece.isPromotable = False
            self.updateWindow()

    def printBoard(self):
        for row in range(0, len(self.Board.Board)):
            for col in range(0, len(self.Board.Board[row])):
                print(self.Board.Board[row][col])

    #Fonction qui permet, � partir d'un clique du joueur, de s�lectionner la pi�ce sur laquelle le joueur a cliqu�
    #Si le joueur a cliqu� sur une pi�ce, cette pi�ce est alors stock�e dans l'attribut selected et on affiche ses mouvements
    #Sinon on supprime les mouvements affich�s et on change de pi�ce
    def select(self, row, col):
        if self.selected:               #Si on a d�j� s�lectionn� une pi�ce
            move = self._move(row, col) #Si on clique sur un d�placement possible pour la pi�ce s�lectionn�e, d�place la pi�ce et retourne True
            if not move:                #Si on clique sur une case qui n'est pas un d�placement de self.selected
                self.selected = None    #On d�selectionne la pi�ce 
                self.select(row, col)   #On re boucle sur la m�thode
        else:
            piece = self.Board.getPiece(row, col)
            if piece != 0 and self.turn == piece.cote:
                self.selected = piece
                self.validMoves = piece.getAvailableMoves(row, col, self.Board.Board)
            else:
                self.validMoves = []

    #Supprime une pi�ce du terrain avec comptage de points
    def remove(self, board, piece, row, col):
        if board[row][col] != 0:
            if board[row][col].cote == Joueur.Regnant:
                board[row][col] = 0
                self.RegnantPiecesLeft -= 1
            else:
                board[row][col] = 0
                self.OpposantPiecesLeft -= 1
        #print("RegnantPiecesLeft : ", self.RegnantPiecesLeft)
        #print("OpposantPiecesLeft : ", self.OpposantPiecesLeft)

    #Affiche en vert les cases o� la pi�ce peut se d�placer (utile pour les d�butant et le d�bug)
    def drawAvailableMoves(self):
        if len(self.validMoves) > 0:
            for pos in self.validMoves:
                row, col = pos[0], pos[1]
                pygame.draw.circle(self.window, green, (col*self.square + self.square//2, row*self.square + self.square//2), self.square//8) #Pour bien mettre au centre du carr� et pas dans un coin

    def drawPromotion(self):
        if self.selected is not None and self.selected.isPromotable == True:
            row, col = self.selected.row, self.selected.col
            pygame.draw.circle(self.window, red, (col*self.square + self.square//2, row*self.square + self.square//2), self.square//8)

    def getPosition(self, x, y):  #M�thode servant � convertir la position du clique de la souris en case de clique de la souris
        row = y//square     #Ligne �gale � position du clique divis� par nb de case du jeu
        col = x//square     # // mais avec les colonnes
        return row, col
