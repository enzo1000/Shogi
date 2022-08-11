from Roi import *

class GeneralDeJade(Roi):
    def __init__(self, square, image, cote, type, row, col):
        super().__init__(square, image, cote, type, row, col)

    def getAvailableMoves(self, row, col, Board):
        super().availableMoves(row, col, Board)


