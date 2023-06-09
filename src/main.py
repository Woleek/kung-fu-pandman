import pygame

import settings as settings
from game import PandmanGame

pygame.init()

screen = pygame.display.set_mode(
    (settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
pygame.display.set_caption('Kung Fu Pandman')

game = PandmanGame(screen)
game.run()
