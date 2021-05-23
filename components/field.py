from components.button import Button

from constants.colors import WHITE


class Field(Button):
    def __init__(self, color: tuple[int, int, int], x: int, y: int, width: int, height: int, text: str = '',
                 cartesian_coordinates: bool = True) -> None:
        super().__init__(color, x, y, width, height, text, cartesian_coordinates)
        self._clicked = False
        self._cannot_be_chosen = False

    def draw_init(self, window) -> None:
        if self._cannot_be_chosen:
            self.draw(window, outline_color=(255, 0, 0))  # temp for testing
        elif self._clicked:
            self.draw(window, outline_color=(0, 0, 255))  # temp for testing
        else:
            self.draw(window, outline_color=WHITE)

    def choose_field(self):
        self._clicked = True

    def prevent_selection(self):
        self._cannot_be_chosen = True
