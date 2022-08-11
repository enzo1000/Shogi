import pygame
import os

widthS, heightS = 800, 800
rows, cols = 9,9
square = widthS//rows

brown = (87,16,16)
white = (255,255,255)

pathPieces = "src\images\pieces"
pathPromotions = "src\images\promotion"

listesPieces = ["cavalier", "fou", "generalDargent", "generalDor", "lancier", "pion", "tour"]
promotions = ["argentDor", "cavalierDor", "chevalDragon", "dragon", "lancierDor", "pionDor"]

piecesReignant = listesPieces + ["roi"]
piecesOpposant = listesPieces + ["generalDeJade"]

imagesPiecesReignant = {}
imagesPiecesOpposant = {}
imagesPromotionsReignant = {}
imagesPromotionsOpposant = {}

#{} pour initialiser un dictionnaire en python et [] pour un tableau
#Dictionnaires accessibles en plus que par des indices, par des mots

#En python, les variables on 2 niveaux de port�s, local ou global.
#En fonction de leur niveau, les variables vont �tre r�pertori�s dans la commande globals() ou locales()
#Ce sont toutes deux des dictionnaires r�pertoriant de nombreuses m�thodes, variables et scripts ...
#Ces deux dictionnaires ne sont pas utilis�s explicitement ici mais implicitement lors d'appel de variables (ce commentaire est � titre informatif)

for piece in piecesReignant:
    imagesPiecesReignant[piece] = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(os.path.join(pathPieces, piece + ".png")), (square, square)), 180)

for piecePromu in promotions:
    imagesPromotionsReignant[piece] = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(os.path.join(pathPieces, piece + ".png")), (square, square)), 180)

for piece in piecesOpposant:
    imagesPiecesOpposant[piece] = pygame.transform.scale(pygame.image.load(os.path.join(pathPieces, piece + ".png")), (square, square))

for piecePromu in promotions:
    imagesPromotionsOpposant[piece] = pygame.transform.scale(pygame.image.load(os.path.join(pathPieces, piece + ".png")), (square, square))