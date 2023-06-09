import random
import threading
import typing

import pygame

import settings as settings

if typing.TYPE_CHECKING:
    from block import Block
    from game import PandmanGame
    from noodle import Noodle
    from pandman import Pandman


class Jombie(threading.Thread):
    """
    Class representing jombie (jade zombie)
    """

    def __init__(self, game: 'PandmanGame', x: int = None, y: int = None, name: str = 'Jombie'):
        """
        Initialize basic jombie parameters like location on the screen, name and image representing it

        Args:
            game (PandmanGame): reference to the game instance
            x (int, optional): location in X axis, defaults to None where it's set as random
            y (int, optional): location in Y axis, defaults to None where it's set as random
            name (str, optional): instance name (for debugging), defaults to 'Jombie'
        """
        threading.Thread.__init__(self)
        self.gname = name
        self.x = x if x else random.randint(0, settings.NUM_BLOCKS_X - 1)
        self.y = y if y else random.randint(0, settings.NUM_BLOCKS_Y - 1)
        self.game = game
        self.image = pygame.transform.scale(pygame.image.load(
            'images/jombie.png'), (settings.BLOCK_SIZE, settings.BLOCK_SIZE))

    def update(self):
        """
        Update jombie position based on player's position and game settings
        """
        with self.game.lock:
            dx, dy = self.get_next_move()
            temp_x = self.x + dx
            temp_y = self.y + dy

            # check for collision with blocks
            if self.game.get_block(temp_x, temp_y) is None:
                self.x = temp_x
                self.y = temp_y
            if self.game.get_block(temp_x, self.y) is None:
                self.x = temp_x
            elif self.game.get_block(self.x, temp_y) is None:
                self.y = temp_y

    def draw(self):
        """
        Draw jombie on the screen
        """
        self.rect = pygame.Rect(self.x * settings.BLOCK_SIZE, self.y *
                                settings.BLOCK_SIZE, settings.BLOCK_SIZE, settings.BLOCK_SIZE)
        with self.game.lock:
            self.game.screen.blit(self.image, self.rect)

    def collides_with(self, other: typing.Union['Block', 'Noodle', 'Pandman']):
        """
        Check for collision with other game object (same coordinates in X and Y axis)

        Args:
            other (Union[Block, Noodle, Pandman]): other game object

        Returns:
            _type_: True if objects collide, False otherwise
        """
        with self.game.lock:
            return self.x == other.x and self.y == other.y

    def get_next_move(self):
        """
        Calculate next move direction based on Pandman's current location, invert that move based on jombie aim and random factor, then set next move in X or Y axis randomly

        Returns:
            Set(int, int): next move values in X and Y axes
        """
        # current Pandman position
        pac_x = self.game.pandman.x
        pac_y = self.game.pandman.y
        dx = dy = 0

        rand = False
        # invert move direction randomly depending on aim factor
        if random.random() > settings.JOMBIE_AIM:
            rand = True

        if self.x < pac_x:
            dx = 1
        elif self.x > pac_x:
            dx = -1
        if self.y < pac_y:
            dy = 1
        elif self.y > pac_y:
            dy = -1

        # move in X or Y axis randomly
        if random.random() > 0.5:
            return (dx, 0) if not rand else (-dx, 0)
        else:
            return (0, dy) if not rand else (0, -dy)
