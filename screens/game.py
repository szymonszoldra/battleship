import pygame
import itertools
from functools import reduce
from random import random, randint
from typing import Union, Tuple

from constants.window import FPS, WIDTH, HEIGHT, FIELD_SIZE, OUTLINE_THICKNESS_THICK
from constants.colors import BUTTON_COLOR, BACKGROUND_COLOR, WHITE
from constants.fonts import FONT, FONT_PATH
from constants.difficulty import EASY, HARD, TEST
from constants.messages import COMPUTER_WON_MESSAGE, YOU_WON_MESSAGE

from components.button import Button
from components.field import Field
from utils.field_processor import FieldProcessor
from exceptions.game import FieldAlreadyShotException


class Game:
    def __init__(self, window, difficulty: str) -> None:
        self._WINDOW = window
        self._difficulty = difficulty
        self._setup_over = False
        self._btn_restart = Button(BUTTON_COLOR, 400, HEIGHT - 80, 200, 80, 'Restart')
        self._btn_quit = Button(BUTTON_COLOR, WIDTH - 400, HEIGHT - 80, 200, 80, 'Menu')
        self._player_fields = [[Field(BACKGROUND_COLOR, 100 + x * FIELD_SIZE + FIELD_SIZE // 2, 150 + y * FIELD_SIZE,
                                      FIELD_SIZE, FIELD_SIZE, (x, y), False) for y in range(10)] for x in range(10)]
        self._computer_fields = [[Field(BACKGROUND_COLOR, 900 + x * FIELD_SIZE + FIELD_SIZE // 2, 150 + y * FIELD_SIZE,
                                        FIELD_SIZE, FIELD_SIZE, (x, y), True) for y in range(10)] for x in range(10)]

        self.process_computer_fields()
        self._ships_to_allocate = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
        self._latest_clicked_field: Union[Tuple[int, int], None] = None

        # randomly selected whether the first move belongs to the player or to the computer
        self._is_player_move: bool = random() < 0.5

        self._possible_shoots = [(x, y) for x in range(10) for y in range(10)]
        self._computer_good_shots = 0
        self._player_good_shots = 0
        self._good_shots_to_win = reduce(lambda a, b: a + b, self._ships_to_allocate)

    def process_computer_fields(self) -> None:
        field_processor = FieldProcessor(self._computer_fields)
        field_processor.choose_fields_for_computer_ships()

    def process_hard_difficulty(self) -> None:
        while len(self._possible_shoots) > 70:
            fields_without_ships = list(
                filter(lambda f: not f.should_shoot_this_field(), itertools.chain.from_iterable(self._player_fields)))

            index = randint(0, len(fields_without_ships) - 1)
            coords = fields_without_ships[index].get_coords()
            if coords in self._possible_shoots:
                self._possible_shoots.remove(coords)

    def draw_buttons(self) -> None:
        self._WINDOW.fill(BACKGROUND_COLOR)
        self._btn_restart.draw(self._WINDOW, font_size=30)
        self._btn_quit.draw(self._WINDOW, font_size=30)

    def draw_init_fields(self) -> None:
        for x in range(10):
            for y in range(10):
                self._player_fields[x][y].draw_init(self._WINDOW)
                self._computer_fields[x][y].draw_init(self._WINDOW)

    def draw_titles(self) -> None:
        user = FONT.render('You', True, WHITE)
        computer = FONT.render('Computer', True, WHITE)

        self._WINDOW.blit(user, (400 - user.get_width() // 2, 80 - user.get_height() // 2))
        self._WINDOW.blit(computer, (WIDTH - 400 - computer.get_width() // 2, 80 - computer.get_height() // 2))

    def reset_fields_in_setup(self) -> None:
        for row in self._player_fields:
            for field in row:
                field.set_temporary_mouse_over(False)

    def setup_horizontal(self, coords: Tuple[int, int], size: int) -> None:
        x, y = coords
        if x > 10 - size:
            return

        field_processor = FieldProcessor(self._player_fields)

        if not field_processor.can_ship_fit((x, y), size, True):
            return

        for _ in range(size):
            self._player_fields[x][y].set_temporary_mouse_over(True)
            x += 1

        if self._latest_clicked_field:
            field_processor.process_horizontal(self._latest_clicked_field, size)
            self._ships_to_allocate.pop(0)

    def setup_vertical(self, coords: Tuple[int, int], size: int) -> None:
        x, y = coords
        if y > 10 - size:
            return

        field_processor = FieldProcessor(self._player_fields)

        if not field_processor.can_ship_fit((x, y), size, False):
            return

        for _ in range(size):
            self._player_fields[x][y].set_temporary_mouse_over(True)
            y += 1

        if self._latest_clicked_field:
            field_processor.process_vertical(self._latest_clicked_field, size)
            self._ships_to_allocate.pop(0)

    def setup(self, mouse_coords: Tuple[int, int], horizontal: bool) -> None:
        if len(self._ships_to_allocate) == 0:
            for field in itertools.chain.from_iterable(self._player_fields):
                field.reset_field_after_setup()

            self._setup_over = True
            if self._difficulty == HARD:
                self.process_hard_difficulty()
            return

        self.reset_fields_in_setup()

        mouse_over = list(filter(lambda f: f.is_mouse_over(mouse_coords),
                                 itertools.chain.from_iterable(self._player_fields)))
        if len(mouse_over) == 0:
            return

        field_coords = mouse_over[0].get_coords()
        current_ship_size = self._ships_to_allocate[0]

        if horizontal:
            self.setup_horizontal(field_coords, current_ship_size)
        else:
            self.setup_vertical(field_coords, current_ship_size)

    def player_move(self) -> None:
        if self._latest_clicked_field:
            x, y = self._latest_clicked_field
            try:
                shot = self._computer_fields[x][y].shoot()
                if shot:
                    self._player_good_shots += 1
            except FieldAlreadyShotException as e:
                print(e)

            print('PLAYER:', self._player_good_shots)

            self._is_player_move = False

    def normal_move(self) -> None:
        index = randint(0, len(self._possible_shoots) - 1)
        x, y = self._possible_shoots.pop(index)
        shot = self._player_fields[x][y].shoot()
        if shot:
            self._computer_good_shots += 1

        print('COMPUTER:', self._computer_good_shots)
        self._is_player_move = True

    def impossible_move(self) -> None:
        fields_to_shoot = list(
            filter(lambda f: f.should_shoot_this_field(), itertools.chain.from_iterable(self._player_fields)))

        index = randint(0, len(fields_to_shoot) - 1)
        ship = fields_to_shoot.pop(index)
        ship.shoot()
        self._computer_good_shots += 1
        print('COMPUTER:', self._computer_good_shots)
        self._is_player_move = True

    def computer_move(self) -> None:
        if self._difficulty == EASY or self._difficulty == HARD:
            self.normal_move()
        else:
            self.impossible_move()

    def play(self) -> None:
        if self._is_player_move:
            self.player_move()
        else:
            self.computer_move()

    def display_winner(self, message: str) -> None:
        pygame.draw.rect(self._WINDOW, BUTTON_COLOR, (WIDTH // 2 - 400, HEIGHT // 2 - 200, 800, 400), 0)
        pygame.draw.rect(self._WINDOW, BACKGROUND_COLOR, (
            WIDTH // 2 - 400 + OUTLINE_THICKNESS_THICK, HEIGHT // 2 - 200 + OUTLINE_THICKNESS_THICK,
            800 - OUTLINE_THICKNESS_THICK * 2,
            400 - OUTLINE_THICKNESS_THICK * 2), 0)
        font = pygame.font.Font(FONT_PATH, 80)
        text = font.render(message, True, WHITE)
        self._WINDOW.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
        pygame.display.update()
        pygame.time.wait(1500)

    def start(self) -> Tuple[str, bool]:
        run = True
        clock = pygame.time.Clock()
        click = False
        setup_horizontal = False
        while run:
            clock.tick(FPS)
            mouse_coords = pygame.mouse.get_pos()

            if self._btn_restart.is_mouse_over(mouse_coords) and click:
                return 'RESTART', True

            if self._btn_quit.is_mouse_over(mouse_coords) and click:
                return 'QUIT', False

            if self._setup_over:
                for x in range(10):
                    for y in range(10):
                        if self._computer_fields[x][y].is_mouse_over(mouse_coords) and click:
                            self._latest_clicked_field = (x, y)
            else:
                for x in range(10):
                    for y in range(10):
                        if self._player_fields[x][y].is_mouse_over(mouse_coords) and click:
                            self._latest_clicked_field = (x, y)

            click = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    click = True

                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    setup_horizontal = not setup_horizontal

            self.draw_buttons()
            self.draw_init_fields()
            self.draw_titles()
            if not self._setup_over:
                self.setup(mouse_coords, setup_horizontal)
            else:
                if self._player_good_shots == self._good_shots_to_win:
                    if self._difficulty == TEST:
                        return YOU_WON_MESSAGE, False

                    self.display_winner(YOU_WON_MESSAGE)
                    return YOU_WON_MESSAGE, True
                elif self._computer_good_shots == self._good_shots_to_win:
                    if self._difficulty == TEST:
                        return COMPUTER_WON_MESSAGE, False

                    self.display_winner(COMPUTER_WON_MESSAGE)
                    return COMPUTER_WON_MESSAGE, True
                else:
                    self.play()
            self._latest_clicked_field = None
            pygame.display.update()
