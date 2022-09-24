import pygame
from .Board import Board
from .constants import *
from .Joueur import *
from .Pieces import *
from copy import copy


class Game:
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

    def updateWindow(self):
        self.Board.drawBoard()
        self.Board.drawPieces()
        self.Board.drawSide()
        self.drawAvailableMoves()
        self.drawPromotion()
        self.drawPara()
        pygame.display.update()

    def checkGame(self):
        if self.checkmate(self.Board):
            if self.turn == Joueur.Opposant:
                print("Regnant wins")
                return True
            else:
                print("Opposant wins")
                return True

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

    def simulateMove(self, piece, row, col):
        if piece == self.Board.Board[row][col]:
            print("YMCMB")

        print(self.Board.Board[row][col])

        pieceRow, pieceCol = piece.row, piece.col
        savePiece = self.Board.Board[row][col]

        if self.Board.Board[row][col] != 0:
            self.Board.Board[row][col] = 0

        self.Board.Board[piece.row][piece.col], self.Board.Board[row][col] = self.Board.Board[row][col], self.Board.Board[piece.row][piece.col]

        kingPos = self.getKingPos(self.Board.Board)
        if kingPos in self.enemiesMoves(piece, self.Board.Board):
            piece.row, piece.col = pieceRow, pieceCol
            self.Board[pieceRow][pieceCol] = piece
            self.Board.Board[row][col] = savePiece
            return False
        else:
            piece.row, piece.col = pieceRow, pieceCol
            self.Board.Board[pieceRow][pieceCol] = piece
            self.Board.Board[pieceRow][pieceCol] = savePiece
            return True

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
        
            kingAvailableMoves = set(getKing.getAvailableMoves(kingPos[0], kingPos[1], Board.Board))
            enemiesMovesSet = set(self.enemiesMoves(getKing, Board.Board))
            kingMoves = kingAvailableMoves - enemiesMovesSet
            set1 = kingAvailableMoves.intersection(enemiesMovesSet)
            possibleMovesToDef = set1.intersection(self.possibleMoves(Board.Board))
            if len(kingMoves) == 0 and len(kingAvailableMoves) != 0 and possibleMovesToDef == 0:
                return True
            else:
                return False
        else:
            return True
        
    def reset(self):
        self.Board = Board(self.Board.width, self.Board.height, rows, cols, square, self.window)
        self.selected = None
        self.RegnantPiecesLeft, self.OpposantPiecesLeft = 20,20
        self.validMoves = []
        
    def changeTurn(self):
        if self.turn == Joueur.Regnant:
            self.turn = Joueur.Opposant
        else:
            self.turn = Joueur.Regnant

    def _move(self, rowVisee, colVisee):
        rowInit, colInit = self.selected.row, self.selected.col
        caseVisee = self.Board.getPiece(rowVisee, colVisee)
        if self.selected and (rowVisee, colVisee) in self.validMoves:
            if caseVisee == 0 or caseVisee.cote != self.selected.cote:

                self.remove(self.Board.Board, self.Board.Board[rowVisee][colVisee], rowVisee, colVisee)
                self.Board.move(self.selected, rowVisee, colVisee)
                self.validMoves = []

                self.promotionPossible(rowVisee, rowInit)
                if self.selected.isPromotable:
                    self.promotionSelected()

                self.changeTurn()
                self.selected.isPromotable = False
                self.selected = None
                return True
        return False

    def promotionSelected(self):
        piece = self.selected
        promotionLoop = False
        while promotionLoop == False:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed()[0]:
                        location = pygame.mouse.get_pos()
                        row, col = self.getPosition(location[0], location[1])
                        if piece.row == row and piece.col == col:
                            self.Board.Board[row][col] = piece.promoted()
                            promotionLoop = True
                        else:
                            promotionLoop = True

    def promotionPossible(self, row, rowInit):
        piece = self.selected
        if piece.type not in pasPromotable:
            if piece.cote == Joueur.Opposant:
                if row <= 2:
                    piece.isPromotable = True
                elif rowInit <= 2:
                    piece.isPromotable = True
                else:
                    piece.isPromotable = False
            else:
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

    def select(self, location):
        row, col = self.getPosition(location[0], location[1])
        if self.selected:
            move = self._move(row, col)
            if not move:
                self.selected = None
                self.select(location)
        else:
            piece = self.Board.getPiece(row, col)
            if piece != 0 and self.turn == piece.cote:
                self.selected = piece
                self.validMoves = piece.getAvailableMoves(row, col, self.Board.Board)
            else:
                self.validMoves = []
                
    def remove(self, board, piece, row, col):
        if board[row][col] != 0:
            if board[row][col].cote == Joueur.Regnant:
                board[row][col] = 0
                self.OpposantPiecesPara.append(piece.type)
            else:
                board[row][col] = 0
                self.RegnantPiecesPara.append(piece.type)

    def drawAvailableMoves(self):
        if len(self.validMoves) > 0:
            for pos in self.validMoves:
                row, col = pos[0], pos[1]
                pygame.draw.circle(self.window, green, (col*self.square + self.square//2, row*self.square + self.square//2), self.square//8)

    def drawPromotion(self):
        if self.selected is not None and self.selected.isPromotable == True:
            row, col = self.selected.row, self.selected.col
            pygame.draw.circle(self.window, red, (col*self.square + self.square//2, row*self.square + self.square//2), self.square//8)

    def getPosition(self, x, y):
        row = y//square
        col = x//square
        return row, col

    def selectPara(self, location):
        row, col = self.getPosition(location[0], location[1])
        if self.Board.Side[row][col] != 0:
            pieceSelect = self.Board.getSideType(row, col)

            if self.turn == Joueur.Opposant:
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

    def dropPara(self, piece, cimetiereRemove):
        pieceFictive = copy(piece)
        BoardFictif = copy(self.Board)

        for row in range(0, len(BoardFictif.Board)):
            for col in range(0, len(BoardFictif.Board[row])):
                if BoardFictif.Board[row][col] == 0:
                    canBePara = True

                    if piece.type == "Pion":
                        canBePara = self.pionVerifColPara(col, BoardFictif.Board)
                    if canBePara:
                        canBePara = self.pieceDeplacementPara(pieceFictive, row)
                    if canBePara:
                        self.validPara.append((row, col))

        self.updateWindow()
        
        canBePara2 = True
        while canBePara2 == True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed()[0]:
                        location = pygame.mouse.get_pos()
                        rowClique, colClique = self.getPosition(location[0], location[1])
                        if (rowClique, colClique) in self.validPara:
                            piece.row = rowClique
                            piece.col = colClique
                            piece.calcPos()
                            self.Board.Board[rowClique][colClique] = piece
                            print(self.Board.Board[rowClique][colClique])

                            self.validPara = []
                            if self.turn == Joueur.Opposant:
                                self.OpposantPiecesPara.remove(cimetiereRemove)
                            else:
                                self.RegnantPiecesPara.remove(cimetiereRemove)
                            self.changeTurn()
                            canBePara2 = False
                        else:
                            self.validPara = []
                            canBePara2 = False
        
    def pieceDeplacementPara(self, pieceFictive, row):
        BoardFictif = []
        for i in range(0, rows):
            BoardFictif.append([0 for i in range(3)])
        if self.turn == Joueur.Opposant:
            if row < 3:
                BoardFictif[row][1] = pieceFictive
                moves = BoardFictif[row][1].getAvailableMoves(row, 1, BoardFictif)
                if len(moves) == 0:
                    return False
            return True
        else:
            if row > 5:
                BoardFictif[row][1] = pieceFictive
                moves = BoardFictif[row][1].getAvailableMoves(row, 1, BoardFictif)
                if len(moves) == 0:
                    return False
            return True

    def pionVerifColPara(self, col, BoardFictif):
        for rowi in range (0, len(BoardFictif)):
            if BoardFictif[rowi][col] != 0:
                if BoardFictif[rowi][col].cote == self.turn:
                    if BoardFictif[rowi][col].type == "Pion":
                        return False
        return True

    def drawPara(self):
        if len(self.validPara) > 0:
            for pos in self.validPara:
                row, col = pos[0], pos[1]
                pygame.draw.circle(self.window, cyan, (col*self.square + self.square//2, row*self.square + self.square//2), self.square//8)