from components.button import Button

from constants.colors import WHITE, RED, GREEN, BLUE

from exceptions.game import FieldAlreadyShotException

from typing import Tuple


class Field(Button):
    def __init__(self, color: Tuple[int, int, int], x: int, y: int, width: int, height: int, coords: Tuple[int, int],
                 computer_field: bool,
                 text: str = '',
                 cartesian_coordinates: bool = True) -> None:
        super().__init__(color, x, y, width, height, text, cartesian_coordinates)
        self._coords = coords
        self._computer_field = computer_field
        self._ship_inside = False
        self._can_be_chosen = True
        self._temporary_mouse_over = False
        self._shot = False
        self._setup_over = False

        if self._computer_field:
            self.set_show_text(False)

    def get_coords(self) -> Tuple[int, int]:
        return self._coords

    def draw_as_computer_field(self, window) -> None:
        if self._shot:
            if self._ship_inside:
                self.draw(window, BLUE, font_size=40)
            else:
                self.draw(window, RED)
        else:
            self.draw(window, WHITE)

    def draw_as_player_field(self, window) -> None:
        if not self._setup_over:
            if not self._can_be_chosen:
                self.draw(window, outline_color=RED)
            elif self._ship_inside:
                self.draw(window, outline_color=BLUE, font_size=40)
            elif self._temporary_mouse_over:
                self.draw(window, outline_color=GREEN)
            else:
                self.draw(window, outline_color=WHITE)
        else:
            if self._shot:
                if self._ship_inside:
                    self.draw(window, BLUE, font_size=40)
                else:
                    self.draw(window, RED)
            else:
                self.draw(window, WHITE, font_size=40)

    def draw_init(self, window) -> None:
        if self._computer_field:
            self.draw_as_computer_field(window)
        else:
            self.draw_as_player_field(window)

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
        self._setup_over = True
        self._can_be_chosen = True

    def shoot(self) -> bool:
        if self._shot:
            raise FieldAlreadyShotException

        self._shot = True
        self.set_show_text(True)
        return self._ship_inside

    def should_shoot_this_field(self) -> bool:
        """ For impossible difficulty only"""
        return self._ship_inside and not self._shot
