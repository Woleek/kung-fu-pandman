from settings import *

class Jombie(threading.Thread):
    def __init__(self, game, x=None, y=None, name='Jombie'):
        threading.Thread.__init__(self) 
        self.gname = name
        self.x = x if x else random.randint(0, NUM_BLOCKS_X - 1)
        self.y = y if y else random.randint(0, NUM_BLOCKS_Y - 1)
        self.game = game
        self.image = pygame.transform.scale(pygame.image.load('images/jombie.png'), (BLOCK_SIZE, BLOCK_SIZE))
        
    def update(self):
        with self.game.lock:
            # print(f"{self.gname} entered critical update section")
            dx, dy = self.get_next_move()
            temp_x = self.x + dx * JOMBIE_SPEED
            temp_y = self.y + dy* JOMBIE_SPEED
            
            if self.game.get_block(temp_x, temp_y) is None:
                self.x = temp_x
                self.y = temp_y
            if self.game.get_block(temp_x, self.y) is None:
                self.x = temp_x
            elif self.game.get_block(self.x, temp_y) is None:
                self.y = temp_y
            
              
    # Metoda rysująca duszka na ekranie
    def draw(self):
        self.rect = pygame.Rect(self.x * BLOCK_SIZE, self.y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
        with self.game.lock:
            self.game.screen.blit(self.image, self.rect)

    # Metoda sprawdzająca kolizję duszka z innym obiektem
    def collides_with(self, other):
        with self.game.lock: 
            return self.x == other.x and self.y == other.y

    # Metoda zwracająca następny ruch duszka
    def get_next_move(self):
        pac_x = self.game.pandman.x
        pac_y = self.game.pandman.y
        dx = dy = 0
        
        rand = False
        if random.random() > JOMBIE_AIM:
            rand = True
            
        if self.x < pac_x:
            dx = 1
        elif self.x > pac_x:
            dx = -1
        if self.y < pac_y:
            dy = 1
        elif self.y > pac_y:
            dy = -1
            
        if random.random() > 0.5:
            return (dx, 0) if not rand else (-dx, 0)
        else:
            return (0, dy) if not rand else (0, -dy)
