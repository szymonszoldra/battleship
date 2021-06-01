import unittest
import pygame
import itertools
from random import randint
from screens.game import Game

from constants.window import WIDTH, HEIGHT
from constants.difficulty import EASY, TEST
from constants.messages import COMPUTER_WON_MESSAGE, YOU_WON_MESSAGE


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

    def test_good_shoot_computer_field(self):
        """
        Player points field is incremented after good shoot
        """

        game = Game(self.WINDOW, EASY)
        game._is_player_move = True

        fields_with_ship = list(filter(lambda f: f._ship_inside, itertools.chain.from_iterable(game._computer_fields)))
        field_with_ship = fields_with_ship[randint(0, len(fields_with_ship) - 1)]
        game._latest_clicked_field = field_with_ship.get_coords()

        score_before = game._player_good_shots
        game.player_move()
        score_after = game._player_good_shots

        self.assertEqual(score_before + 1, score_after)

    def test_shoot_empty_field(self):
        """
        Player points field is not incremented after shooting empty field
        """
        game = Game(self.WINDOW, EASY)
        game._is_player_move = True

        fields_without_ship = list(
            filter(lambda f: not f._ship_inside, itertools.chain.from_iterable(game._computer_fields)))
        field_without_ship = fields_without_ship[randint(0, len(fields_without_ship) - 1)]
        game._latest_clicked_field = field_without_ship.get_coords()

        score_before = game._player_good_shots
        game.player_move()
        score_after = game._player_good_shots

        self.assertEqual(score_before, score_after)

    def test_win_game(self):
        """
        Win game against computer
        """
        game = Game(self.WINDOW, TEST)

        game._setup_over = True
        game._player_good_shots = game._good_shots_to_win
        message, _ = game.start()

        self.assertEqual(message, YOU_WON_MESSAGE)

    def test_lose_game(self):
        """
        Lose game against computer
        """
        game = Game(self.WINDOW, TEST)

        game._setup_over = True
        game._computer_good_shots = game._good_shots_to_win
        message, _ = game.start()

        self.assertEqual(message, COMPUTER_WON_MESSAGE)


if __name__ == '__main__':
    unittest.main()
