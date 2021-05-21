import pygame
from typing import Callable
from constants.difficulty import EASY, HARD, IMPOSSIBLE
from constants.colors import BUTTON_COLOR, BACKGROUND_COLOR
from constants.window import WIDTH, HEIGHT, FPS

from components.Button import Button


class Options:
    def __init__(self, window):
        self._WINDOW = window
        self._btn_easy = Button(BUTTON_COLOR, WIDTH // 2, HEIGHT // 4, 200, 80, EASY)
        self._btn_hard = Button(BUTTON_COLOR, WIDTH // 2, HEIGHT // 4 * 2, 200, 80, HARD)
        self._btn_impossible = Button(BUTTON_COLOR, WIDTH // 2, HEIGHT // 4 * 3, 200, 80, IMPOSSIBLE)

    def draw_options(self):
        self._WINDOW.fill(BACKGROUND_COLOR)
        self._btn_easy.draw(self._WINDOW, font_size=30)
        self._btn_hard.draw(self._WINDOW, font_size=30)
        self._btn_impossible.draw(self._WINDOW, font_size=30)

        pygame.display.update()

    def set_options(self, setter: Callable):
        run = True
        clock = pygame.time.Clock()
        click = False
        while run:
            clock.tick(FPS)
            mouse_coords = pygame.mouse.get_pos()

            if self._btn_easy.is_mouse_over(mouse_coords) and click:
                setter(EASY)
                run = False

            if self._btn_hard.is_mouse_over(mouse_coords) and click:
                setter(HARD)
                run = False

            if self._btn_impossible.is_mouse_over(mouse_coords) and click:
                setter(IMPOSSIBLE)
                run = False

            click = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    click = True

            self.draw_options()
