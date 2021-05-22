import pygame

from constants.window import FPS, WIDTH, HEIGHT
from constants.colors import BUTTON_COLOR, BACKGROUND_COLOR

from components.button import Button


class Game:
    def __init__(self, window, difficulty: str):
        self._WINDOW = window
        self._difficulty = difficulty
        self._btn_restart = Button(BUTTON_COLOR, WIDTH // 3, HEIGHT - 80, 200, 80, 'Restart')
        self._btn_quit = Button(BUTTON_COLOR, WIDTH // 3 * 2, HEIGHT - 80, 200, 80, 'Menu')

    def draw_buttons(self):
        self._WINDOW.fill(BACKGROUND_COLOR)
        self._btn_restart.draw(self._WINDOW, font_size=30)
        self._btn_quit.draw(self._WINDOW, font_size=30)

        pygame.display.update()

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
