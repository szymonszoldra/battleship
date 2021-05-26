from components.button import Button

from constants.colors import WHITE, RED, GREEN, BLUE


class Field(Button):
    def __init__(self, color: tuple[int, int, int], x: int, y: int, width: int, height: int, coords: tuple[int, int],
                 text: str = '',
                 cartesian_coordinates: bool = True) -> None:
        super().__init__(color, x, y, width, height, text, cartesian_coordinates)
        self._coords = coords
        self._ship_inside = False
        self._can_be_chosen = True
        self._temporary_mouse_over = False

    def get_coords(self) -> tuple[int, int]:
        return self._coords

    def draw_init(self, window) -> None:
        if not self._can_be_chosen:
            self.draw(window, outline_color=RED)
        elif self._ship_inside:
            self.draw(window, outline_color=WHITE, font_size=40)
        elif self._temporary_mouse_over:
            self.draw(window, outline_color=GREEN)
        else:
            self.draw(window, outline_color=WHITE)

    def choose_field(self, size: str) -> None:
        self._ship_inside = True
        self._text = size  # Protected

    def prevent_selection(self) -> None:
        self._can_be_chosen = False

    def can_field_be_chosen(self) -> bool:
        return self._can_be_chosen and not self._ship_inside

    def set_temporary_mouse_over(self, value: bool) -> None:
        if self.can_field_be_chosen():
            self._temporary_mouse_over = value

    def reset_field_after_setup(self) -> None:
        self._can_be_chosen = True
