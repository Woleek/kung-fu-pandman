import random
import threading
import typing

import pygame

import settings
from block import Block
from jombie import Jombie
from noodle import Noodle
from pandman import Pandman

class PandmanGame:
    """
    Class representing the actual game logic with update and drawing operations for the screen
    """

    def __init__(self, screen: pygame.Surface):
        """Initialize basic game parameters and start threads for game objects

        Args:
            screen (pygame.Surface): display of the game
        """
        self.score = Score(self, 0)
        self.life = LifeBar(self, settings.LIFE)
        self.timer = Timer(self)
        self.game_over = False
        self.draw_over = False
        self.screen = screen
        self.lock = threading.Lock()
        self.game_over_img = pygame.transform.scale(pygame.image.load(
            'images/over.png'), (settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))

        # Pandman
        self.pandman = Pandman(self)
        self.pandman.start()
        self.pandman.join()

        # jombies
        self.jombies = []
        for idx in range(settings.NUM_JOMBIES):
            self.jombies.append(Jombie(self, name=f'Jombie_{idx+1}'))
            self.jombies[idx].start()
            self.jombies[idx].join()

        # blocks
        self.blocks = []
        for x in range(settings.NUM_BLOCKS_X):
            for y in range(settings.NUM_BLOCKS_Y):
                if (x == 0 or x == settings.NUM_BLOCKS_X - 1 or y == 0 or y == settings.NUM_BLOCKS_Y - 1) or (random.random() < settings.BLOCKS_DENSITY) or (x == settings.NUM_BLOCKS_X // 2 and y == settings.NUM_BLOCKS_Y // 2):
                    self.blocks.append(Block(self, x, y))

        # noodles
        self.noodles = []

    def handle_events(self):
        """
        Handle game over event
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_over = True

    def get_block(self, x: int, y: int):
        """
        Get block with coordinates x, y if there is one

        Args:
            x (int): X axis value
            y (int): Y axis value

        Returns:
            Union[Block, None]: block object or None if block was not found
        """
        for block in self.blocks:
            if block.x == x and block.y == y:
                return block

    def update(self):
        """
        Update game objects, score and time based on game logic
        """

        def update_object(object: typing.Union['Pandman', 'Noodle', 'Jombie']):
            """
            Run any game object's update method

            Args:
                object (Union[Pandman, Noodle, Jombie]): object to update
            """
            object.update()

        # check if life dropped to 0
        if self.life.val <= 0:
            self.draw_over = True
            self.score.x = settings.SCREEN_WIDTH // 2
            self.score.y = settings.SCREEN_HEIGHT * 0.8
            self.score.font = pygame.font.SysFont("agencyfb", 100)

        # update pandman
        update_object(self.pandman)

        # check if pandman ate noodle
        for noodle in self.noodles:
            if noodle['present'] and self.pandman.collides_with(noodle['object']):
                self.score.val += 1
                noodle['present'] = False
                noodle['rest'] = settings.NOODLE_REST
                self.timer.update_time(10)

        # check if jombie bumped into pandman
        for jombie in self.jombies:
            update_object(jombie)
            if self.pandman.collides_with(jombie):
                self.life.val -= 1
                self.pandman.x = settings.NUM_BLOCKS_X // 2
                self.pandman.y = settings.NUM_BLOCKS_Y // 2

            # check if jombie ate noodle
            for noodle in self.noodles:
                if noodle['present'] and jombie.collides_with(noodle['object']):
                    noodle['present'] = False
                    noodle['rest'] = settings.NOODLE_REST
                    self.timer.update_time(-10)

        # update timer
        if self.timer.counter <= settings.FRAMERATE:
            self.timer.counter += 1
        else:
            self.timer.counter = 0
            self.timer.update_time(1)

        # update number of noodles based on game time
        n_noodles = self.timer.time // 60 + 1  # new noodle for every 1 min in game
        while len(self.noodles) != n_noodles:
            if len(self.noodles) < n_noodles:
                self.noodles.append(
                    {'object': Noodle(self), 'rest': 0, 'present': False})
                # check if noodle spawned on block
                while True:  
                    collstion = False
                    for block in self.blocks:
                        if self.noodles[-1]['object'].collides_with(block):
                            collstion = True
                            self.noodles[-1]['object'].x = random.randint(
                                0, settings.NUM_BLOCKS_X - 1)
                            self.noodles[-1]['object'].y = random.randint(
                                0, settings.NUM_BLOCKS_Y - 1)
                            break
                    if not collstion:
                        break
                self.noodles[-1]['object'].start()
                self.noodles[-1]['object'].join()
            else:
                del self.noodles[-1]

    def draw(self):
        """
        Draw game objects, points and timer on the screen
        """
        self.screen.fill(settings.BLACK)

        def draw_object(object: typing.Union['Pandman', 'Noodle', 'Jombie', 'Block', 'Score', 'LifeBar', 'Timer']):
            """
            Run any game object's draw method

            Args:
                object (Union[Pandman, Noodle, Jombie, Block, Score, LifeBar, Timer]): object to draw
            """
            object.draw()

        # draw game over image if game ended
        if self.draw_over:
            rect = self.game_over_img.get_rect()
            with self.lock:
                self.screen.blit(self.game_over_img, (rect.x, rect.y))
            draw_object(self.score)
            pygame.display.flip()
            return

        # draw blocks
        for block in self.blocks:
            draw_object(block)

        # draw pandman
        draw_object(self.pandman)

        # draw jombies
        for jombie in self.jombies:
            draw_object(jombie)

        # draw noodles
        for noodle in self.noodles:
            # spawn noodle
            if noodle['rest'] == 0 and not noodle['present']:
                noodle['rest'] = settings.NOODLE_REST
                noodle['present'] = True

            # tick noodle rest time
            elif not noodle['present']:
                noodle['rest'] -= 1

            # draw noodle
            if noodle['present']:
                draw_object(noodle['object'])

        # draw life, timer and score
        draw_object(self.score)
        draw_object(self.life)
        draw_object(self.timer)

        pygame.display.flip()

    def run(self):
        """
        Run game logic
        """
        clock = pygame.time.Clock()
        while not self.game_over:
            self.handle_events()
            self.update()
            self.draw()
            clock.tick(settings.FRAMERATE)


class Timer(object):
    """
    Class represeting ingame clock
    """

    def __init__(self, game: 'PandmanGame'):
        """
        Initialize basic ingame clock parameters

        Args:
            game (PandmanGame): reference to game instance
        """
        self.game = game
        self.time = 0
        self.counter = 0
        self.x = 40
        self.y = 30
        self.font = pygame.font.SysFont("agencyfb", 40)
        self.lock = threading.Lock()

    def update_time(self, val: int):
        """Update timer with given value

        Args:
            val (int): positive or negative value added to the timer
        """
        with self.lock:
            self.time += val

    def _calc_time(self):
        """
        Calculate h:m:s time for displaying

        Returns:
            str: h:m:s string representing current ingame time
        """
        temp_time = self.time

        # hours
        h = temp_time // 3600
        temp_time = temp_time % 3600

        # minuters
        m = temp_time // 60
        temp_time = temp_time % 60

        # seconds
        s = temp_time
        return f"{h:2}:{m:2}:{s:2}"

    def draw(self):
        """
        Draw timer on the screen
        """
        text = self.font.render(self._calc_time(), True, (255, 255, 255))
        with self.game.lock:
            self.game.screen.blit(text, (self.x, self.y))


class LifeBar(object):
    def __init__(self, game: 'PandmanGame', life: int):
        """
        Initialize basic lifebar parameters

        Args:
            game (PandmanGame): reference to game instance
            life (int): starting life points
        """
        self.game = game
        self.val = life

        self.image = pygame.transform.scale(
            pygame.image.load('images/heart.png'), (40, 40))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 30, settings.SCREEN_HEIGHT - 80

    def draw(self):
        """
        Draw lifebar on the screen
        """
        for life in range(self.val):
            with self.game.lock:
                self.game.screen.blit(
                    self.image, (self.rect.x + life*self.rect.width, self.rect.y))


class Score(object):
    def __init__(self, game: 'PandmanGame', score: int = 0):
        """
        Initialize basic score counter parameners

        Args:
            game (PandmanGame): reference to game instance
            score (int): starting player points, defaults to 0
        """
        # Game variables and settings
        self.val = score
        self.game = game
        self.x = settings.SCREEN_WIDTH - 80
        self.y = settings.SCREEN_HEIGHT - 80
        self.font = pygame.font.SysFont("agencyfb", 40)

    def draw(self):
        """
        Draw score on the screen
        """
        text = self.font.render(str(self.val), True, (255, 255, 255))
        with self.game.lock:
            self.game.screen.blit(text, (self.x, self.y))
