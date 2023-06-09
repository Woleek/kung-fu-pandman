import random
import threading
import typing

import pygame

import settings as settings

if typing.TYPE_CHECKING:
    from block import Block
    from game import PandmanGame
    from jombie import Jombie
    from pandman import Pandman


class Noodle(threading.Thread):
    """
    Class representing noodles that Pandman tries to collect during the game to earn points
    """

    def __init__(self, game: 'PandmanGame', x: int = None, y: int = None):
        """
        Initialize basic noodle parameters like location on the screen and image representing it

        Args:
            game (PandmanGame): reference to game instance
            x (int, optional): location in X axis, defaults to None where it's set as random
            y (int, optional): location in Y axis, defaults to None where it's set as random
        """
        threading.Thread.__init__(self)
        self.x = x if x else random.randint(0, settings.NUM_BLOCKS_X - 1)
        self.y = y if y else random.randint(0, settings.NUM_BLOCKS_Y - 1)
        self.game = game
        self.image = pygame.transform.scale(pygame.image.load(
            'images/noodle.png'), (settings.BLOCK_SIZE, settings.BLOCK_SIZE))

    def draw(self):
        """
        Draw noodle on the screen
        """
        self.rect = pygame.Rect(
            self.x * settings.BLOCK_SIZE, self.y * settings.BLOCK_SIZE, settings.BLOCK_SIZE, settings.BLOCK_SIZE)
        with self.game.lock:
            self.game.screen.blit(self.image, self.rect)

    def collides_with(self, other: typing.Union['Pandman', 'Block', 'Jombie']):
        """
        Check for collision with other game object (same coordinates in X and Y axis)

        Args:
            other (Union[Pandman, Block, Jombie]): other game object

        Returns:
            bool: True if objects collide, False otherwise
        """
        with self.game.lock:
            return self.x == other.x and self.y == other.y
