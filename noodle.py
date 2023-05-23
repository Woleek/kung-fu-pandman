from settings import *


class Noodle(threading.Thread):
    def __init__(self, game, x=None, y=None):
        threading.Thread.__init__(self)
        self.x = x if x else random.randint(0, NUM_BLOCKS_X - 1)
        self.y = y if y else random.randint(0, NUM_BLOCKS_Y - 1)
        self.game = game
        self.image = pygame.transform.scale(pygame.image.load('images/noodle.png'), (BLOCK_SIZE, BLOCK_SIZE))
    
    # Metoda rysująca noodle na ekranie
    def draw(self):
        self.rect = pygame.Rect(self.x * BLOCK_SIZE, self.y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
        with self.game.lock:
            self.game.screen.blit(self.image, self.rect)

    # Metoda sprawdzająca zjedzenie noodle
    def collides_with(self, other):
        with self.game.lock: 
            return self.x == other.x and self.y == other.y
