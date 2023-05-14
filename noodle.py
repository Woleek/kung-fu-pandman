from settings import *


class Noodle(threading.Thread):
    def __init__(self, game, x=None, y=None):
        self.x = x if x else random.randint(0, NUM_BLOCKS_X - 1)
        self.y = y if y else random.randint(0, NUM_BLOCKS_Y - 1)
        self.game = game
        threading.Thread.__init__(self)
    
    # Metoda rysująca noodle na ekranie
    def draw(self):
        rect = pygame.Rect(self.x * BLOCK_SIZE, self.y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
        with self.game.lock:
            pygame.draw.rect(self.game.screen, WHITE, rect)

    # Metoda sprawdzająca zjedzenie noodle
    def collides_with(self, other):
        with self.game.lock: 
            return self.x == other.x and self.y == other.y
