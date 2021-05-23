from components.button import Button

from constants.colors import WHITE, BUTTON_COLOR


class Field(Button):
    def __init__(self, color: tuple[int, int, int], x: int, y: int, width: int, height: int, text: str = '',
                 cartesian_coordinates: bool = True) -> None:
        super().__init__(color, x, y, width, height, text, cartesian_coordinates)
        self._clicked = False

    def draw_init(self, window) -> None:
        if self._clicked:
            self.draw(window, outline_color=(255, 0, 0))
        else:
            self.draw(window, outline_color=WHITE)

    def choose_field(self):
        self._clicked = True
