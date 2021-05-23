from components.button import Button

from constants.colors import WHITE


class Field(Button):
    def __init__(self, color: tuple[int, int, int], x: int, y: int, width: int, height: int, coords: tuple[int, int],
                 text: str = '',
                 cartesian_coordinates: bool = True) -> None:
        super().__init__(color, x, y, width, height, text, cartesian_coordinates)
        self._coords = coords
        self._clicked = False
        self._can_be_chosen = True

    def get_coords(self) -> tuple[int, int]:
        return self._coords

    def draw_init(self, window) -> None:
        if not self._can_be_chosen:
            self.draw(window, outline_color=(255, 0, 0))  # temp for testing
        elif self._clicked:
            self.draw(window, outline_color=(0, 0, 255))  # temp for testing
        else:
            self.draw(window, outline_color=WHITE)

    def choose_field(self) -> None:
        self._clicked = True

    def prevent_selection(self) -> None:
        self._can_be_chosen = False

    def can_field_be_chosen(self) -> bool:
        return self._can_be_chosen and not self._clicked
