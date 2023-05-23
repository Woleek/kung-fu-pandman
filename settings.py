import random
import pygame
import threading
from concurrent.futures import ThreadPoolExecutor

# Ustawienia gry
FRAMERATE = 10
SCREEN_WIDTH = 1840
SCREEN_HEIGHT = 1000
BLOCK_SIZE = 30
BLOCKS_DENSITY = 0.05
NUM_BLOCKS_X = SCREEN_WIDTH // BLOCK_SIZE
NUM_BLOCKS_Y = SCREEN_HEIGHT // BLOCK_SIZE
PANDMAN_SPEED = 1
JOMBIE_SPEED = 1
JOMBIE_AIM = 0.8
NUM_JOMBIES = 4
NOODLE_REST = 30
LIFE = 5
game_over_img = pygame.transform.scale(pygame.image.load('images/over.png'), (SCREEN_WIDTH, SCREEN_HEIGHT))

# Kolory
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)