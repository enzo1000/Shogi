import pygame
import os

widthS, heightS = 800, 800
rows, cols = 9,9
square = widthS//rows

brown = (87,16,16)
white = (255,255,255)

pathPieces = "src\images\pieces"
pathPromotions = "src\images\promotion"

pieces = ["roi", "generalDeJade", "cavalier", "fou", "generalDargent", "generalDor", "lancier", "pion", "tour"]
promotions = ["argentDor", "cavalierDor", "chevalDragon", "dragon", "lancierDor", "pionDor"]

imagesPieces = {}   
imagesPromotions = {}   #{} pour initialiser un dictionnaire en python et [] pour un tableau
                        #Dictionnaires accessibles en plus que par des indices, par des mots

#En python, les variables on 2 niveaux de portés, local ou global.
#En fonction de leur niveau, les variables vont être répertoriés dans la commande globals() ou locales()
#Ce sont toutes deux des dictionnaires répertoriant de nombreuses méthodes, variables et scripts ...

for piece in pieces:
    imagesPieces[piece] = pygame.transform.scale(pygame.image.load(os.path.join(pathPieces, piece + ".png")), (square, square))

for piece in promotions:
    imagesPromotions[piece] = pygame.transform.scale(pygame.image.load(os.path.join(pathPromotions, piece + ".png")), (square, square))