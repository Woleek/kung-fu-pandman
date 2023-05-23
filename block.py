from settings import *

class Block:
    def __init__(self, game, x, y):
        self.x = x
        self.y = y
        self.game = game
        self.image = pygame.transform.scale(pygame.image.load('images/block.png'), (BLOCK_SIZE, BLOCK_SIZE))
    
    def draw(self):
        self.rect = pygame.Rect(self.x * BLOCK_SIZE, self.y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
        with self.game.lock:
            self.game.screen.blit(self.image, self.rect)
    
    def collides_with(self, other):
        return self.x == other.x and self.y == other.y