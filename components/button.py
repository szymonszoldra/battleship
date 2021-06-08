import pygame
from constants.colors import WHITE
from constants.window import OUTLINE_THICKNESS
from constants.fonts import FONT_PATH

from typing import Tuple


class Button:
    def __init__(self, color: Tuple[int, int, int], x: int, y: int, width: int, height: int, text: str = '',
                 cartesian_coordinates: bool = True) -> None:
        self._color = color
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._text = text
        self._show_text = True

        if cartesian_coordinates:
            self._x -= self._width // 2
            self._y -= self._height // 2

    def is_mouse_over(self, mouse_position: Tuple[int, int]) -> bool:
        # mouse_position is a tuple of (x, y) mouse coordinates
        is_mouse_inside_x = self._x < mouse_position[0] < self._x + self._width
        is_mouse_inside_y = self._y < mouse_position[1] < self._y + self._height

        return is_mouse_inside_x and is_mouse_inside_y

    def set_show_text(self, value: bool) -> None:
        self._show_text = value

    def draw(self, window, outline_color: Tuple[int, int, int] = None, font_size: int = 10) -> None:
        if outline_color:
            pygame.draw.rect(window, outline_color, (self._x, self._y, self._width, self._height), 0)
            pygame.draw.rect(window, self._color, (
                self._x + OUTLINE_THICKNESS, self._y + OUTLINE_THICKNESS, self._width - OUTLINE_THICKNESS * 2,
                self._height - OUTLINE_THICKNESS * 2), 0)
        else:
            pygame.draw.rect(window, self._color, (self._x, self._y, self._width, self._height), 0)

        if self._text != '' and self._show_text:
            font = pygame.font.Font(FONT_PATH, font_size)
            text = font.render(self._text, True, WHITE)
            window.blit(text, (self._x + (self._width // 2 - text.get_width() // 2),
                               self._y + (self._height // 2 - text.get_height() // 2)))
