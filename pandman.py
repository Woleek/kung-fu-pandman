from settings import *

class Pandman(threading.Thread):
    def __init__(self, game):
        threading.Thread.__init__(self)  
        self.x = NUM_BLOCKS_X // 2
        self.y = NUM_BLOCKS_Y // 2
        self.game = game
        self.image = pygame.transform.scale(pygame.image.load('images/pandman.png'), (BLOCK_SIZE, BLOCK_SIZE))
        
    def update(self):
        keys = pygame.key.get_pressed()
        with self.game.lock:
            # print("Pandman entered critical update section")
            temp_x, temp_y = self.get_next_move(keys)
            if self.game.get_block(temp_x, temp_y) is not None:
                return
            else:
                if temp_x != self.x:
                    if temp_x < self.x:
                        if temp_x >= 0:
                            self.x = temp_x
                        else:
                            self.x = NUM_BLOCKS_X-1
                    elif temp_x < NUM_BLOCKS_X:
                        self.x = temp_x
                    else:
                        self.x = 0
                else:
                    if temp_y < self.y:
                        if temp_y >= 0:
                            self.y = temp_y
                        else:
                            self.y = NUM_BLOCKS_Y-1
                    elif temp_y < NUM_BLOCKS_Y:
                        self.y = temp_y
                    else:
                        self.y = 0

    def collides_with(self, other):
        with self.game.lock: 
            return self.x == other.x and self.y == other.y

    def get_next_move(self, keys):
        temp_x = self.x
        temp_y = self.y
        if keys[pygame.K_LEFT]:
            temp_x = self.x - PANDMAN_SPEED
        elif keys[pygame.K_RIGHT]:
            temp_x = self.x + PANDMAN_SPEED
        elif keys[pygame.K_UP]:
            temp_y = self.y - PANDMAN_SPEED
        elif keys[pygame.K_DOWN]:
            temp_y = self.y + PANDMAN_SPEED
        return temp_x, temp_y
        
    
    def draw(self):
        self.rect = pygame.Rect(self.x * BLOCK_SIZE, self.y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
        with self.game.lock:
            self.game.screen.blit(self.image, self.rect)