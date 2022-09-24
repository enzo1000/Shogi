import pygame
import sys

from src.constants import *
from src.Game import *

clock = pygame.time.Clock()
window = pygame.display.set_mode((1200, 900))

def main():
    run = True
    gameOver = False
    FPS = 60
    game = Game(widthS, heightS, rows, cols, square, window)

    while run:
        clock.tick(FPS)

        game.updateWindow()
        if game.checkGame():
            gameOver = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                #quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and gameOver:
                    game.reset()
                    pass
                    
            if event.type == pygame.MOUSEBUTTONDOWN and not gameOver:
                if pygame.mouse.get_pressed()[0]:
                    location = pygame.mouse.get_pos()
                    if location[0] <= widthS and location[1] <= heightS:
                        game.select(location)
                        pass
                    else:
                        game.selectPara(location)
                        pass
main()