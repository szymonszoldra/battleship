import pygame
import itertools
from typing import Union

from constants.window import FPS, WIDTH, HEIGHT, FIELD_SIZE
from constants.colors import BUTTON_COLOR, BACKGROUND_COLOR, WHITE
from constants.fonts import FONT

from components.button import Button
from components.field import Field
from utils.field_processor import FieldProcessor


class Game:
    def __init__(self, window, difficulty: str) -> None:
        self._WINDOW = window
        self._difficulty = difficulty
        self._setup_over = False
        self._btn_restart = Button(BUTTON_COLOR, 400, HEIGHT - 80, 200, 80, 'Restart')
        self._btn_quit = Button(BUTTON_COLOR, WIDTH - 400, HEIGHT - 80, 200, 80, 'Menu')
        self._player_fields = [[Field(BACKGROUND_COLOR, 100 + i * FIELD_SIZE + FIELD_SIZE // 2, 150 + j * FIELD_SIZE,
                                      FIELD_SIZE, FIELD_SIZE, (i, j)) for j in range(10)] for i in range(10)]
        self._computer_fields = [[Field(BACKGROUND_COLOR, 900 + i * FIELD_SIZE + FIELD_SIZE // 2, 150 + j * FIELD_SIZE,
                                        FIELD_SIZE, FIELD_SIZE, (i, j)) for j in range(10)] for i in range(10)]

        self.process_computer_fields()
        self._ships_to_allocate = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
        self._latest_clicked_field: Union[tuple[int, int], None] = None

    def process_computer_fields(self):
        field_processor = FieldProcessor(self._computer_fields)
        field_processor.choose_fields_for_computer_ships()

    def draw_buttons(self) -> None:
        self._WINDOW.fill(BACKGROUND_COLOR)
        self._btn_restart.draw(self._WINDOW, font_size=30)
        self._btn_quit.draw(self._WINDOW, font_size=30)

    def draw_init_fields(self) -> None:
        for i in range(10):
            for j in range(10):
                self._player_fields[i][j].draw_init(self._WINDOW)
                self._computer_fields[i][j].draw_init(self._WINDOW)

    def draw_titles(self) -> None:
        user = FONT.render('You', True, WHITE)
        computer = FONT.render('Computer', True, WHITE)

        self._WINDOW.blit(user, (400 - user.get_width() // 2, 80 - user.get_height() // 2))
        self._WINDOW.blit(computer, (WIDTH - 400 - computer.get_width() // 2, 80 - computer.get_height() // 2))

    def reset_fields_in_setup(self) -> None:
        for i in range(10):
            for j in range(10):
                self._player_fields[i][j].set_temporary_mouse_over(False)

    def setup(self, mouse_coords: tuple[int, int], horizontal: bool) -> None:
        if len(self._ships_to_allocate) == 0:
            self._setup_over = True
            return

        self.reset_fields_in_setup()

        mouse_over = list(filter(lambda f: f.is_mouse_over(mouse_coords),
                                 itertools.chain.from_iterable(self._player_fields)))
        if len(mouse_over) == 0:
            return
        x, y = mouse_over[0].get_coords()
        current_ship = self._ships_to_allocate[0]
        field_processor = FieldProcessor(self._player_fields)

        if horizontal:
            if x > 10 - current_ship:
                return

            if not field_processor.can_ship_fit((x, y), current_ship, True):
                return

            for _ in range(current_ship):
                self._player_fields[x][y].set_temporary_mouse_over(True)
                x += 1

            if self._latest_clicked_field:
                field_processor.process_horizontal(self._latest_clicked_field, current_ship)
                self._ships_to_allocate.pop(0)

        else:
            if y > 10 - current_ship:
                return

            if not field_processor.can_ship_fit((x, y), current_ship, False):
                return

            for _ in range(current_ship):
                self._player_fields[x][y].set_temporary_mouse_over(True)
                y += 1

            if self._latest_clicked_field:
                field_processor.process_vertical(self._latest_clicked_field, current_ship)
                self._ships_to_allocate.pop(0)

    def start(self) -> bool:
        run = True
        clock = pygame.time.Clock()
        click = False
        setup_horizontal = False
        while run:
            clock.tick(FPS)
            mouse_coords = pygame.mouse.get_pos()

            if self._btn_restart.is_mouse_over(mouse_coords) and click:
                return True

            if self._btn_quit.is_mouse_over(mouse_coords) and click:
                return False

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

            self._latest_clicked_field = None
            pygame.display.update()
            if len(self._ships_to_allocate) == 0:
                print('GAME CAN START')
