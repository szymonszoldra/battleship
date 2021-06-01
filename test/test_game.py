import unittest
import pygame
from random import randint

from constants.window import WIDTH, HEIGHT
from constants.difficulty import EASY
from screens.game import Game
from exceptions.game import FieldAlreadyShotException


class FieldTest(unittest.TestCase):
    WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))

    def test_shoot_empty_field(self):
        """
        Shoot empty field\n
        """
        game = Game(self.WINDOW, EASY)
        x = randint(0, 9)
        y = randint(0, 9)
        field = game._computer_fields[x][y]
        self.assertEqual(field._shot, False)
        field.shoot()
        self.assertEqual(field._shot, True)

    def test_throws_FieldAlreadyShotException(self):
        """
        Shooting the same field again raises FieldAlreadyShotException
        """
        game = Game(self.WINDOW, EASY)
        x = randint(0, 9)
        y = randint(0, 9)
        field = game._computer_fields[x][y]
        field.shoot()

        self.assertRaises(FieldAlreadyShotException, field.shoot)


if __name__ == '__main__':
    unittest.main()
