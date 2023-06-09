import typing

import pygame

import settings as settings

if typing.TYPE_CHECKING:
    from game import PandmanGame
    from jombie import Jombie
    from noodle import Noodle
    from pandman import Pandman


class Block:
    """
    Class representing game block (wall)
    """

    def __init__(self, game: 'PandmanGame', x: int, y: int):
        """
        Initialize basic block parameters like location on the screen and image representing it

        Args:
            game (PandmanGame): reference to the game instance
            x (int): location in X axis
            y (int): location in Y axis
        """

        self.x = x
        self.y = y
        self.game = game
        self.image = pygame.transform.scale(pygame.image.load(
            'images/block.png'), (settings.BLOCK_SIZE, settings.BLOCK_SIZE))

    def draw(self):
        """
        Draw block on the screen
        """
        self.rect = pygame.Rect(self.x * settings.BLOCK_SIZE, self.y *
                                settings.BLOCK_SIZE, settings.BLOCK_SIZE, settings.BLOCK_SIZE)
        with self.game.lock:
            self.game.screen.blit(self.image, self.rect)

    def collides_with(self, other: typing.Union['Jombie', 'Noodle', 'Pandman']):
        """
        Check for collision with other game object (same coordinates in X and Y axis)

        Args:
            other (Union[Jombie, Noodle, Pandman]): other game object

        Returns:
            bool: True if objects collide, False otherwise
        """
        return self.x == other.x and self.y == other.y
