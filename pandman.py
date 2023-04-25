from settings import *

class Pandman:
    def __init__(self, game):
        self.x = NUM_BLOCKS_X // 2
        self.y = NUM_BLOCKS_Y // 2
        self.game = game
        
    def update(self):
        keys = pygame.key.get_pressed()
        with self.game.lock:
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

    def collides_with(self, other):
        return self.x == other.x and self.y == other.y

    def draw(self):
        rect = pygame.Rect(self.x * BLOCK_SIZE, self.y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
        with self.game.lock:
            pygame.draw.rect(self.game.screen, YELLOW, rect)