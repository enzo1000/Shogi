import pygame
import os

widthS, heightS = 900, 900  #Multiple de 9 sans virgules sinon on peut out of bound avec la souris
rows, cols = 9,9
square = widthS//rows

brown = (87,16,16)
white = (255,255,255)
green = (0, 255, 0)
red = (255, 0, 0)

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

#{} pour initialiser un dictionnaire en python et [] pour un tableau
#Dictionnaires accessibles en plus que par des indices, par des mots

#En python, les variables on 2 niveaux de portés, local ou global.
#En fonction de leur niveau, les variables vont être répertoriés dans la commande globals() ou locales()
#Ce sont toutes deux des dictionnaires répertoriant de nombreuses méthodes, variables et scripts ...
#Ces deux dictionnaires ne sont pas utilisés explicitement ici mais implicitement lors d'appel de variables (ce commentaire est à titre informatif)

for piece in piecesReignant:
    imagesPiecesRegnant[piece] = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(os.path.join(pathPieces, piece + ".png")), (square, square)), 180)

for piecePromu in promotions:
    imagesPromotionsRegnant[piecePromu] = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(os.path.join(pathPromotions, piecePromu + ".png")), (square, square)), 180)

for piece in piecesOpposant:
    imagesPiecesOpposant[piece] = pygame.transform.scale(pygame.image.load(os.path.join(pathPieces, piece + ".png")), (square, square))

for piecePromu in promotions:
    imagesPromotionsOpposant[piecePromu] = pygame.transform.scale(pygame.image.load(os.path.join(pathPromotions, piecePromu + ".png")), (square, square))