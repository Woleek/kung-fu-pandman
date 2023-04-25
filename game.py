from settings import *
from ghost import Ghost
from pandman import Pandman
from block import Block


# Klasa reprezentująca grę
class PandmanGame:
    def __init__(self, screen):
        self.score = 0
        self.game_over = False
        self.screen = screen
        self.lock = threading.Lock()
        self.basenik_zagrozen = ThreadPoolExecutor()
        
        self.pandman = Pandman(self)
        
        self.ghosts = []
        for _ in range(NUM_GHOSTS):
            self.ghosts.append(Ghost(self))
        
        self.blocks = []
        for x in range(NUM_BLOCKS_X):
            for y in range(NUM_BLOCKS_Y):
                if (x == 0 or x == NUM_BLOCKS_X - 1 or y == 0 or y == NUM_BLOCKS_Y - 1) or (random.random() < BLOCKS_DENSITY):
                    self.blocks.append(Block(self, x, y)) 
                    
    def get_block(self, x, y):
        for block in self.blocks:
            if block.x == x and block.y == y:
                return block
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_over = True
                self.basenik_zagrozen.shutdown(wait=False)
    
    def update(self):
        
        def update_object(object):
            self.basenik_zagrozen.submit(object.update).result()
        
        update_object(self.pandman)
        
        for ghost in self.ghosts:
            update_object(ghost)
        
    def draw(self):
        self.screen.fill(BLACK)
        
        def draw_object(object):
            self.basenik_zagrozen.submit(object.draw).result()
                
        for block in self.blocks:
            block.draw()
        
        draw_object(self.pandman)
        
        for ghost in self.ghosts:
            draw_object(ghost)
            
        pygame.display.flip()
    
    def run(self):
        clock = pygame.time.Clock()
        while not self.game_over:
            self.handle_events()
            self.update()
            self.draw()
            clock.tick(20)