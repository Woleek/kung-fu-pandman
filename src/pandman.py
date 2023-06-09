import threading
import typing

import pygame

import settings

if typing.TYPE_CHECKING:
    from block import Block
    from game import PandmanGame
    from jombie import Jombie
    from noodle import Noodle


class Pandman(threading.Thread):
    """
    Class representing Pandman (player)
    """

    def __init__(self, game: 'PandmanGame'):
        """
        Initialize basic Pandman parameters like location on the screen and image representing it

        Args:
            game (PandmanGame): reference to game instance
        """
        threading.Thread.__init__(self)
        self.x = settings.NUM_BLOCKS_X // 2
        self.y = settings.NUM_BLOCKS_Y // 2
        self.game = game
        self.image = pygame.transform.scale(pygame.image.load(
            'images/pandman.png'), (settings.BLOCK_SIZE, settings.BLOCK_SIZE))

    def update(self):
        """
        Update Pandman position based on player's keyboard interactions
        """
        keys = pygame.key.get_pressed()
        with self.game.lock:
            temp_x, temp_y = self.get_next_move(keys)
            # check for collision with block
            if self.game.get_block(temp_x, temp_y) is not None:
                return
            else:
                # move in X axis
                if temp_x != self.x:
                    # move left
                    if temp_x < self.x:
                        if temp_x >= 0:
                            self.x = temp_x
                        # move from left end to right
                        else:
                            self.x = settings.NUM_BLOCKS_X-1
                    # move right
                    elif temp_x < settings.NUM_BLOCKS_X:
                        self.x = temp_x
                    # move from right end to left
                    else:
                        self.x = 0
                # move in Y axis
                else:
                    # move up
                    if temp_y < self.y:
                        if temp_y >= 0:
                            self.y = temp_y
                        # move from bottom end to top
                        else:
                            self.y = settings.NUM_BLOCKS_Y-1
                    # move down
                    elif temp_y < settings.NUM_BLOCKS_Y:
                        self.y = temp_y
                    # move from top end to bottom
                    else:
                        self.y = 0

    def collides_with(self, other: typing.Union['Jombie', 'Block', 'Noodle']):
        """
        Check for collision with other game object (same coordinates in X and Y axis)

        Args:
            other (Union[Jombie, Block, Noodle]): other game object

        Returns:
            bool: True if objects collide, False otherwise
        """
        with self.game.lock:
            return self.x == other.x and self.y == other.y

    def get_next_move(self, keys: typing.Sequence[bool]):
        """
        Calculate next location in X or Y axis based on currently pressed key

        Args:
            keys (Sequence[bool]): pressed keys

        Returns:
           Set(int, int) : next x and y values
        """
        temp_x = self.x
        temp_y = self.y
        if keys[pygame.K_LEFT]:
            temp_x = self.x - 1
        elif keys[pygame.K_RIGHT]:
            temp_x = self.x + 1
        elif keys[pygame.K_UP]:
            temp_y = self.y - 1
        elif keys[pygame.K_DOWN]:
            temp_y = self.y + 1
        return (temp_x, temp_y)

    def draw(self):
        """
        Draw Pandman on the screen
        """
        self.rect = pygame.Rect(self.x * settings.BLOCK_SIZE, self.y *
                                settings.BLOCK_SIZE, settings.BLOCK_SIZE, settings.BLOCK_SIZE)
        with self.game.lock:
            self.game.screen.blit(self.image, self.rect)
