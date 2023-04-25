from settings import *

class Block:
    def __init__(self, game, x, y):
        self.x = x
        self.y = y
        self.game = game
    
    def draw(self):
        rect = pygame.Rect(self.x * BLOCK_SIZE, self.y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
        with self.game.lock:
            pygame.draw.rect(self.game.screen, BLUE, rect)
    
    def collides_with(self, other):
        return self.x == other.x and self.y == other.y