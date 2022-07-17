from turtle import width
import pygame

from src.constants import *

pygame.init()

clock = pygame.time.Clock() #La même que Time.deltaTime() sous unity
window = pygame.display.set_mode((widthS, heightS))

def get_position(x,y):  #Méthode servant à convertir la position du clique de la souris en case de clique de la souris
    row = y//square     #Ligne égale à position du clique divisé par nb de case du jeu
    col = x//square     # // mais avec les colonnes

def main():
    run = True
    
    while run:
        clock.tick(60)  #Prise en compte seulement du 60 FPS (pour un jeu d'échec ça va)
        
        window.blit(imagesPieces["roi"], (50,50))  #On affiche le roi en position 50 50

        pygame.display.update()

        for event in pygame.event.get():    #Définitions des évènements qui peuvent arriver durant la partie
            if event.type == pygame.QUIT:   #Si l'on quitte le jeu
                run = False
                quit()

            if event.type == pygame.KEYDOWN:    #Si l'on appuie sur barre espace et que l'on est en game_over alors on reset la partie
                if event.type == pygame.K_SPACE and gameOver:  #game_over est une variable proche de run mais qui ne viendra pas couper l'application
                    pass

            if event.type == pygame.MOUSEBUTTONDOWN and not gameOver:  #Si l'on appuie sur la souris et que l'on est pas en game_over alors
                if pygame.mouse.get_pressed()[0]:                       #Si clique gauche
                    location = pygame.mouse.get_pos()                   #On vient récupérer les coordonnées du clique afin de vérifier s'il y a une pièce ou autre dessous
                    row, col = get_position(location[0], location[1])   #On vient récupérer la case du clique
main()