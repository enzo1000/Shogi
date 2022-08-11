import pygame
from .Board import newBoard
from .constants import *
from .Joueur import *
from copy import deepcopy

class Game:
    def __init__(self, Width, Height, Rows, Cols, Square, Win):
        self.Win = Win
        self.Board = newBoard(Width, Height, Rows, Cols, Square, Win)
        self.Square = Square
        self.selected = None
        self.turn = Joueur.Regnant
        self.validMoves = []
        self.RegnantPiecesLeft = 20
        self.OpposantPiecesLeft = 20

    def updateWindow(self):
        self.Board.drawBoard()
        self.Board.drawPieces()
        self.drawAvailableMoves()
        pygame.display.update()

    def reset(self):
        self.Board = newBoard(widthS, heightS, rows, cols, square, Win)
        self.selected = None
        self.RegnantPiecesLeft, self.OpposantPiecesLeft = 20,20
        self.validMoves = []

    def changeTurn(self):
        if self.turn == Joueur.Regnant:
            self.turn = Joueur.Opposant
        else:
            self.turn = Joueur.Regnant

    def select(self, row, col):
        if self.selected:
            move = self._move(row, col)

            if not move: 
                self.selected = None
                self.selected(row, col)

            piece = self.Board.getPiece(row, col)
            if piece != 0 and self.turn == piece.cote:
                self.selected = piece
                self.validMoves = piece.getAvailableMoves(row, col, self.Board.Board)

    def _move(self, row, col):
        piece = self.Board.getPiece(row, col)
        if self.selected and (row, col) in self.validMoves:
            if piece == 0 or piece.cote != self.selected.cote:
                if self.simulateMove(self.selected, row, col):
                    self.remove(self.selected, row, col):
                        self.Board.move(self.Board.Board, piece, row, col)
                        self.changeTurn()
                        self.validMoves = []
                        self.selected = None
                        return True
                    return False
                
            return False

    def remove(self, board, piece, row, col):
        if piece != 0:
            board[row][col] = 0
            if piece.cote == Joueur.Regnant:
                self.RegnantPiecesLeft -= 1
            else:
                self.OpposantPiecesLeft -= 1

    def drawAvailableMoves(self):
        if len(self.validMoves) > 0:
            for pos in self.validMoves:
                row, col = pos[0], pos[1]
                pygame.draw.circle(self.Win, green, (col*self.Square + self.Square//2), self.Square//8) #Pour bien mettre au centre du carré et pas dans un coin
