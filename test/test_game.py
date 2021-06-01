import unittest
import pygame
import itertools

from screens.game import Game


from constants.window import WIDTH, HEIGHT
from constants.difficulty import EASY


class GameTest(unittest.TestCase):
    WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))

    def test_different_ships_allocation(self):
        """
        Every new game has different computer ships allocation
        """
        game1 = Game(self.WINDOW, EASY)
        game2 = Game(self.WINDOW, EASY)

        game1_fields = list(itertools.chain.from_iterable(game1._computer_fields))
        game2_fields = list(itertools.chain.from_iterable(game2._computer_fields))

        game1_ships = ''.join([field._text if field._text else '0' for field in game1_fields])
        game2_ships = ''.join([field._text if field._text else '0' for field in game2_fields])

        self.assertNotEqual(game1_ships, game2_ships)


if __name__ == '__main__':
    unittest.main()
