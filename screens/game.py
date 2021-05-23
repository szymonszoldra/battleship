import pygame

from constants.window import FPS, WIDTH, HEIGHT, FIELD_SIZE
from constants.colors import BUTTON_COLOR, BACKGROUND_COLOR, WHITE
from constants.fonts import FONT

from components.button import Button
from components.field import Field


class Game:
    def __init__(self, window, difficulty: str) -> None:
        self._WINDOW = window
        self._difficulty = difficulty
        self._btn_restart = Button(BUTTON_COLOR, 400, HEIGHT - 80, 200, 80, 'Restart')
        self._btn_quit = Button(BUTTON_COLOR, WIDTH - 400, HEIGHT - 80, 200, 80, 'Menu')
        self._player_fields = [[Field(BACKGROUND_COLOR, 100 + i * FIELD_SIZE + FIELD_SIZE // 2, 150 + j * FIELD_SIZE,
                                      FIELD_SIZE, FIELD_SIZE) for j in range(10)] for i in range(10)]
        self._computer_fields = [[Field(BACKGROUND_COLOR, 900 + i * FIELD_SIZE + FIELD_SIZE // 2, 150 + j * FIELD_SIZE,
                                        FIELD_SIZE, FIELD_SIZE) for j in range(10)] for i in range(10)]

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

    def play(self) -> bool:
        run = True
        clock = pygame.time.Clock()
        click = False
        while run:
            clock.tick(FPS)
            mouse_coords = pygame.mouse.get_pos()

            if self._btn_restart.is_mouse_over(mouse_coords) and click:
                return True

            if self._btn_quit.is_mouse_over(mouse_coords) and click:
                return False

            click = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    click = True

            self.draw_buttons()
            self.draw_init_fields()
            self.draw_titles()
            pygame.display.update()
