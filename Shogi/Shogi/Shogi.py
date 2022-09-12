#coding=utf-8
import pygame

from src.constants import *
from src.Game import *
from src.pieces.Pieces import *

pygame.init()

clock = pygame.time.Clock() #La m�me que Time.deltaTime() sous unity
window = pygame.display.set_mode((1200, 900)) #On cr�er un �cran (Surface)

def getPosition(x,y):  #M�thode servant � convertir la position du clique de la souris en case de clique de la souris
    row = y//square     #Ligne �gale � position du clique divis� par nb de case du jeu
    col = x//square     # // mais avec les colonnes
    return row, col

def main():
    run = True
    gameOver = False
    FPS = 60
    game = Game(widthS, heightS, rows, cols, square, window)

    while run:
        clock.tick(FPS)  #Prise en compte seulement du 60 FPS (pour un jeu d'�chec �a va)

        #window.blit(imagesPiecesRegnant["roi"], (50, 50))  #On affiche le roi en position 50 50
        #window.blit(imagesPiecesOpposant["generalDeJade"], (150, 150))

        game.updateWindow()
        if game.checkGame():
            gameOver = True

        for event in pygame.event.get():    #D�finitions des �v�nements qui peuvent arriver durant la partie
            if event.type == pygame.QUIT:   #Si l'on quitte le jeu
                run = False
                quit()

            if event.type == pygame.KEYDOWN:    #Si l'on appuie sur barre espace et que l'on est en game_over alors on reset la partie
                if event.key == pygame.K_SPACE and gameOver:  #game_over est une variable proche de run mais qui ne viendra pas couper l'application
                    game.reset()
                    
            if event.type == pygame.MOUSEBUTTONDOWN and not gameOver:  #Si l'on appuie sur la souris et que l'on est pas en game_over alors
                if pygame.mouse.get_pressed()[0]:                       #Si clique gauche
                    location = pygame.mouse.get_pos()                   #On vient r�cup�rer les coordonn�es du clique afin de v�rifier s'il y a une pi�ce ou autre dessous
                    if location[0] <= widthS and location[1] <= heightS:
                        game.select(location)
                    else:
                        game.selectPara(location)
main()