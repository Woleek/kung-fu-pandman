import pygame
import random
import threading

# Ustawienia gry
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
BLOCK_SIZE = 20
NUM_BLOCKS_X = SCREEN_WIDTH // BLOCK_SIZE
NUM_BLOCKS_Y = SCREEN_HEIGHT // BLOCK_SIZE
PANDMAN_SPEED = 1
GHOST_SPEED = 0
NUM_GHOSTS = 4

# Kolory
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Inicjalizacja Pygame
pygame.init()

# Tworzenie okna
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Pacman')

# Klasa reprezentująca grę
class PandmanGame:
    def __init__(self):
        self.score = 0
        self.game_over = False
        self.lock = threading.Lock()
        
        self.pandman = Pandman(self)
        
        # self.ghosts = []
        # for idx in range(NUM_GHOSTS):
        #     self.ghosts.append(Ghost(self, idx, idx))
        
        self.blocks = []
        for x in range(NUM_BLOCKS_X):
            for y in range(NUM_BLOCKS_Y):
                if (x == 0 or x == NUM_BLOCKS_X - 1 or y == 0 or y == NUM_BLOCKS_Y - 1) or (random.random() < 0.2):
                    self.blocks.append(Block(x, y))
                    
    def get_block(self, x, y):
        for block in self.blocks:
            if block.x == x and block.y == y:
                return block
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_over = True
    
    def update(self):
        self.pandman.update()
        
        # for ghost in self.ghosts:
        #     ghost.update()
        
        for block in self.blocks:
            if self.pandman.collides_with(block):
                self.pandman.undo_move()
        #     for ghost in self.ghosts:
        #         if ghost.collides_with(block):
        #             ghost.undo_move()
    
    def draw(self):
        screen.fill(BLACK)
        
        self.pandman.draw()
        
        for block in self.blocks:
            block.draw()
        
        # for ghost in self.ghosts:
        #     ghost.draw()
            
        pygame.display.flip()
    
    def run(self):
        clock = pygame.time.Clock()
        while not self.game_over:
            self.handle_events()
            self.update()
            self.draw()
            clock.tick(20)
            
# Klasa reprezentująca postać Pacmana
class Pandman:
    def __init__(self, game):
        self.x = NUM_BLOCKS_X // 2
        self.y = NUM_BLOCKS_Y // 2
        self.game = game
        
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            temp_x = self.x - PANDMAN_SPEED
            if self.game.get_block(temp_x, self.y) is not None:
                return
            if temp_x >= 0:
                self.x = temp_x
            else:
                self.x = NUM_BLOCKS_X-1
        elif keys[pygame.K_RIGHT]:
            temp_x = self.x + PANDMAN_SPEED
            if self.game.get_block(temp_x, self.y) is not None:
                return
            if temp_x < NUM_BLOCKS_X:
                self.x = temp_x
            else:
                self.x = 0
        elif keys[pygame.K_UP]:
            temp_y = self.y - PANDMAN_SPEED
            if self.game.get_block(self.x, temp_y) is not None:
                return
            if temp_y >= 0:
                self.y = temp_y
            else:
                self.y = NUM_BLOCKS_Y-1
        elif keys[pygame.K_DOWN]:
            temp_y = self.y + PANDMAN_SPEED
            if self.game.get_block(self.x, temp_y) is not None:
                return
            if temp_y < NUM_BLOCKS_Y:
                self.y = temp_y
            else:
                 self.y = 0
                 
            
        # if self.game.get_block(self.next_x, self.next_y) is not None:
        #     # ruch na pole z blokadą
        #     return

    def collides_with(self, other):
        return self.x == other.x and self.y == other.y

    def draw(self):
        rect = pygame.Rect(self.x * BLOCK_SIZE, self.y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
        pygame.draw.rect(screen, YELLOW, rect)

# Klasa reprezentująca blok w grze
class Block:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def draw(self):
        rect = pygame.Rect(self.x * BLOCK_SIZE, self.y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
        pygame.draw.rect(screen, BLUE, rect)
    
    def collides_with(self, other):
        return self.x == other.x and self.y == other.y

game = PandmanGame()
game.run()