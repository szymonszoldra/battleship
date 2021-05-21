import pygame


class Button:
    def __init__(self, color: tuple[int, int, int], x: int, y: int, width: int, height: int, text: str = '',
                 cartesian_coordinates: bool = True):
        self._color = color
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._text = text

        if cartesian_coordinates:
            self._x -= self._width // 2
            self._y -= self._height // 2

    def is_mouse_over(self, mouse_position: tuple[int, int]):
        # mouse_position is a tuple of (x, y) mouse coordinates
        is_mouse_inside_x = self._x < mouse_position[0] < self._x + self._width
        is_mouse_inside_y = self._y < mouse_position[1] < self._y + self._height

        return is_mouse_inside_x and is_mouse_inside_y

    def draw(self, window, outline_color: tuple[int, int, int] = None, font_size: int = 10, ):
        if outline_color:
            pygame.draw.rect(window, outline_color, (self._x, self._y, self._width, self._height), 0)
            pygame.draw.rect(window, self._color, (self._x + 2, self._y + 2, self._width - 4, self._height - 4), 0)
        else:
            pygame.draw.rect(window, self._color, (self._x, self._y, self._width, self._height), 0)

        if self._text != '':
            font = pygame.font.SysFont('Cascadia Code', font_size)
            white_color = (255, 255, 255)
            text = font.render(self._text, True, white_color)
            window.blit(text, (self._x + (self._width // 2 - text.get_width() // 2),
                               self._y + (self._height // 2 - text.get_height() // 2)))
