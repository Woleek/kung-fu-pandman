import random
import pygame
import threading
from concurrent.futures import ThreadPoolExecutor

# Ustawienia gry
SCREEN_WIDTH = 1840
SCREEN_HEIGHT = 1000
BLOCK_SIZE = 20
BLOCKS_DENSITY = 0.05
NUM_BLOCKS_X = SCREEN_WIDTH // BLOCK_SIZE
NUM_BLOCKS_Y = SCREEN_HEIGHT // BLOCK_SIZE
PANDMAN_SPEED = 1
GHOST_SPEED = 1
GHOST_AIM = 0.8
NUM_GHOSTS = 4

# Kolory
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)