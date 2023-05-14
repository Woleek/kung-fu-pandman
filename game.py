from settings import *
from ghost import Ghost
from pandman import Pandman
from block import Block
from noodle import Noodle


# Klasa reprezentująca grę
class PandmanGame:
    def __init__(self, screen):
        self.score = Score(self, 0)
        self.life = LifeBar(self, LIFE)
        self.game_over = False
        self.draw_over = False
        self.screen = screen
        self.lock = threading.Lock()
        # self.basenik_zagrozen = ThreadPoolExecutor()
        
        # Pandman
        self.pandman = Pandman(self)
        self.pandman.start()
        self.pandman.join()
        
        # ghosts
        self.ghosts = []
        for idx in range(NUM_GHOSTS):
            self.ghosts.append(Ghost(self, name=f'Ghost_{idx+1}'))
            self.ghosts[idx].start()
            self.ghosts[idx].join()
        
        # blocks
        self.blocks = []
        for x in range(NUM_BLOCKS_X):
            for y in range(NUM_BLOCKS_Y):
                if (x == 0 or x == NUM_BLOCKS_X - 1 or y == 0 or y == NUM_BLOCKS_Y - 1) or (random.random() < BLOCKS_DENSITY):
                    self.blocks.append(Block(self, x, y)) 
                    
        # noodle
        self.noodle_rest = NOODLE_REST
        self.noodle_present = False
                    
    def get_block(self, x, y):
        for block in self.blocks:
            if block.x == x and block.y == y:
                return block
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_over = True
                # self.basenik_zagrozen.shutdown(wait=False)
    
    def update(self):
        
        def update_object(object):
            # self.basenik_zagrozen.submit(object.update).result()
            object.update()
        
        update_object(self.pandman)
        if self.noodle_present and self.pandman.collides_with(self.noodle):
            self.score.val += 1
            self.noodle_present = False
            self.noodle_rest = NOODLE_REST
        
        for ghost in self.ghosts:
            update_object(ghost)
            if self.pandman.collides_with(ghost):
                self.life.val -= 1
                self.pandman.x = NUM_BLOCKS_X // 2
                self.pandman.y = NUM_BLOCKS_Y // 2
                
        if self.life.val <= 0:
            self.draw_over = True
            self.score.x = SCREEN_WIDTH // 2
            self.score.y = SCREEN_HEIGHT * 0.8
            self.score.font = pygame.font.SysFont("agencyfb", 100)
        
    def draw(self):
        self.screen.fill(BLACK)
        
        def draw_object(object):
            # self.basenik_zagrozen.submit(object.draw).result()
            object.draw()
        
        if self.draw_over:
            rect = game_over_img.get_rect()
            with self.lock:
                self.screen.blit(game_over_img, (rect.x, rect.y))
            draw_object(self.score)
            pygame.display.flip()
            return        
                
        for block in self.blocks:
            block.draw()
        
        draw_object(self.pandman)
        
        for ghost in self.ghosts:
            draw_object(ghost)
            
        if self.noodle_rest == 0 and not self.noodle_present:
            self.noodle_rest = NOODLE_REST
            self.noodle_present = True
            
            self.noodle = Noodle(self)
            self.noodle.start()
            self.noodle.join()
        elif not self.noodle_present:
            self.noodle_rest -= 1
            
        if self.noodle_present:
            draw_object(self.noodle)
            
        draw_object(self.score)
        draw_object(self.life)
            
        pygame.display.flip()
    
    def run(self):
        clock = pygame.time.Clock()
        while not self.game_over:
            self.handle_events()
            self.update()
            self.draw()
            clock.tick(10)
            
            
class LifeBar(object):
    def __init__(self, game, life):
        # Game variables and settings
        self.game = game
        self.val = life
        
        self.image = pygame.transform.scale(pygame.image.load('images/heart.png'), (40, 40))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 0, SCREEN_HEIGHT - 60
            
    def draw(self):
        for life in range(self.val):
            with self.game.lock:
                self.game.screen.blit(self.image, (self.rect.x + life*self.rect.width, self.rect.y))
            
class Score(object):
    def __init__(self, game, score):
        # Game variables and settings
        self.val = score
        self.game = game
        self.x = SCREEN_WIDTH - 50
        self.y = SCREEN_HEIGHT - 60
        self.font = pygame.font.SysFont("agencyfb", 40)
        
    def draw(self):
        text = self.font.render(str(self.val), True, (255, 255, 255))
        with self.game.lock:
            self.game.screen.blit(text, (self.x, self.y))