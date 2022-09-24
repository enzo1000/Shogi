import pygame
import os

widthS, heightS = 900, 900
rows, cols = 9,9
square = widthS//rows

brown = (87,16,16)
white = (255,255,255)
green = (0, 255, 0)
red = (255, 0, 0)
cyan = (0, 255, 255)

pathPieces = "src\images\pieces"
pathPromotions = "src\images\promotion"

listesPieces = ["cavalier", "fou", "generalDargent", "generalDor", "lancier", "pion", "tour"]
promotions = ["argentDor", "cavalierDor", "chevalDragon", "dragon", "lancierDor", "pionDor"]
pasPromotable = ["ArgentDor", "CavalierDor", "ChevalDragon", "Dragon", "LancierDor", "PionDor", "Roi", "GeneralDeJade", "GeneralDor"]

piecesReignant = listesPieces + ["roi"]
piecesOpposant = listesPieces + ["generalDeJade"]

imagesPiecesRegnant = {}
imagesPiecesOpposant = {}
imagesPromotionsRegnant = {}
imagesPromotionsOpposant = {}

for piece in piecesReignant:
    imagesPiecesRegnant[piece] = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(os.path.join(pathPieces, piece + ".png")), (square, square)), 180)

for piecePromu in promotions:
    imagesPromotionsRegnant[piecePromu] = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(os.path.join(pathPromotions, piecePromu + ".png")), (square, square)), 180)

for piece in piecesOpposant:
    imagesPiecesOpposant[piece] = pygame.transform.scale(pygame.image.load(os.path.join(pathPieces, piece + ".png")), (square, square))

for piecePromu in promotions:
    imagesPromotionsOpposant[piecePromu] = pygame.transform.scale(pygame.image.load(os.path.join(pathPromotions, piecePromu + ".png")), (square, square))