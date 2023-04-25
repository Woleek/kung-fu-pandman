from game import PandmanGame
from settings import *

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Kung Fu Pandman')

game = PandmanGame(screen)
game.run()