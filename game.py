from settings import *
from jombie import Jombie
from pandman import Pandman
from block import Block
from noodle import Noodle


# Klasa reprezentująca grę
class PandmanGame:
    def __init__(self, screen):
        self.score = Score(self, 0)
        self.life = LifeBar(self, LIFE)
        self.timer = Timer(self)
        self.game_over = False
        self.draw_over = False
        self.screen = screen
        self.lock = threading.Lock()
        
        # Pandman
        self.pandman = Pandman(self)
        self.pandman.start()
        self.pandman.join()
        
        # jombies
        self.jombies = []
        for idx in range(NUM_JOMBIES):
            self.jombies.append(Jombie(self, name=f'Jombie_{idx+1}'))
            self.jombies[idx].start()
            self.jombies[idx].join()
        
        # blocks
        self.blocks = []
        for x in range(NUM_BLOCKS_X):
            for y in range(NUM_BLOCKS_Y):
                if (x == 0 or x == NUM_BLOCKS_X - 1 or y == 0 or y == NUM_BLOCKS_Y - 1) or (random.random() < BLOCKS_DENSITY):
                    self.blocks.append(Block(self, x, y)) 
                    
        # noodles
        self.noodles = []
                    
    def get_block(self, x, y):
        for block in self.blocks:
            if block.x == x and block.y == y:
                return block
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_over = True
    
    def update(self):
        
        # function to run any object's update
        def update_object(object):
            object.update()
            
        # check if life dropped to 0
        if self.life.val <= 0:
            self.draw_over = True
            self.score.x = SCREEN_WIDTH // 2
            self.score.y = SCREEN_HEIGHT * 0.8
            self.score.font = pygame.font.SysFont("agencyfb", 100)
        
        # update pandman
        update_object(self.pandman)
        
        # check if pandman ate noodle
        for noodle in self.noodles:
            if noodle['present'] and self.pandman.collides_with(noodle['object']):
                self.score.val += 1
                noodle['present'] = False
                noodle['rest'] = NOODLE_REST
                self.timer.update_time(10)
        
        # check if jombie bumped into pandman
        for jombie in self.jombies:
            update_object(jombie)
            if self.pandman.collides_with(jombie):
                self.life.val -= 1
                self.pandman.x = NUM_BLOCKS_X // 2
                self.pandman.y = NUM_BLOCKS_Y // 2
            
            # check if jombie ate noodle
            for noodle in self.noodles:
                if noodle['present'] and jombie.collides_with(noodle['object']):
                    noodle['present'] = False
                    noodle['rest'] = NOODLE_REST
                    self.timer.update_time(-10)
            
        # update timer
        if self.timer.counter <= FRAMERATE:
            self.timer.counter += 1
        else:
            self.timer.counter = 0
            self.timer.update_time(1)
            
        # update number of noodles based on game time
        n_noodles = self.timer.time // 60 + 1 # new noodle for every 1 min in game
        while len(self.noodles) != n_noodles:
            if len(self.noodles) < n_noodles:
                self.noodles.append({'object':Noodle(self), 'rest':0, 'present':False})
                self.noodles[-1]['object'].start()
                self.noodles[-1]['object'].join()
            else:
                del self.noodles[-1]
        
    def draw(self):
        self.screen.fill(BLACK)
        
        # function to run any object's draw
        def draw_object(object):
            object.draw()
        
        # draw game over screen
        if self.draw_over:
            rect = game_over_img.get_rect()
            with self.lock:
                self.screen.blit(game_over_img, (rect.x, rect.y))
            draw_object(self.score)
            pygame.display.flip()
            return        
                
        # draw blocks
        for block in self.blocks:
            block.draw()
        
        # draw pandman
        draw_object(self.pandman)
        
        # draw jombies
        for jombie in self.jombies:
            draw_object(jombie)
            
        # 
        for noodle in self.noodles:
            if noodle['rest'] == 0 and not noodle['present']:
                noodle['rest'] = NOODLE_REST
                noodle['present'] = True
                
            elif not noodle['present']:
                noodle['rest'] -= 1
                
            if noodle['present']:
                draw_object(noodle['object'])
            
        draw_object(self.score)
        draw_object(self.life)
        draw_object(self.timer)
            
        pygame.display.flip()
    
    def run(self):
        clock = pygame.time.Clock()
        while not self.game_over:
            self.handle_events()
            self.update()
            self.draw()
            clock.tick(FRAMERATE)

class Timer(object):
    def __init__(self, game):
        # Game variables and settings
        self.game = game
        self.time = 0
        self.counter = 0
        self.x = 40
        self.y = 30
        self.font = pygame.font.SysFont("agencyfb", 40)
        self.lock = threading.Lock()
        
    def update_time(self, val):
        with self.lock:
            self.time += val
        
    def _calc_time(self):
        temp_time = self.time
        
        h = temp_time // 360
        temp_time = temp_time % 360
        
        m = temp_time // 60
        temp_time = temp_time % 60
        
        s = temp_time
        return f"{h:2}:{m:2}:{s:2}"
        
        
    def draw(self):
        text = self.font.render(self._calc_time(), True, (255, 255, 255))
        with self.game.lock:
            self.game.screen.blit(text, (self.x, self.y))    
            
class LifeBar(object):
    def __init__(self, game, life):
        # Game variables and settings
        self.game = game
        self.val = life
        
        self.image = pygame.transform.scale(pygame.image.load('images/heart.png'), (40, 40))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 30, SCREEN_HEIGHT - 80
            
    def draw(self):
        for life in range(self.val):
            with self.game.lock:
                self.game.screen.blit(self.image, (self.rect.x + life*self.rect.width, self.rect.y))
            
class Score(object):
    def __init__(self, game, score):
        # Game variables and settings
        self.val = score
        self.game = game
        self.x = SCREEN_WIDTH - 80
        self.y = SCREEN_HEIGHT - 80
        self.font = pygame.font.SysFont("agencyfb", 40)
        
    def draw(self):
        text = self.font.render(str(self.val), True, (255, 255, 255))
        with self.game.lock:
            self.game.screen.blit(text, (self.x, self.y))