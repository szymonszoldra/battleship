import random
from components.field import Field
from typing import List, Tuple

import itertools


class FieldProcessor:
    def __init__(self, fields: List[List[Field]]) -> None:
        self._fields = fields

    def get_prevented_fields(self) -> List[Tuple[int, int]]:
        return list(map(lambda field: field.get_coords(), filter(lambda f: not f.can_field_be_chosen(),
                                                                 itertools.chain.from_iterable(self._fields))))

    def is_field_prevented(self, field: Tuple[int, int]) -> bool:
        return field in self.get_prevented_fields()

    def can_ship_fit(self, starting_pair: Tuple[int, int], length: int, horizontal: bool) -> bool:
        unavailable_fields = self.get_prevented_fields()
        x, y = starting_pair
        if horizontal:
            for _ in range(length):
                if (x, y) in unavailable_fields:
                    return False
                x += 1
            return True
        else:
            for _ in range(length):
                if (x, y) in unavailable_fields:
                    return False
                y += 1
            return True

    def process_horizontal(self, pair: Tuple[int, int], size: int) -> None:
        x, y = pair
        if x != 0:
            if y != 0:
                self._fields[x - 1][y - 1].prevent_selection()
            self._fields[x - 1][y].prevent_selection()
            if y != 9:
                self._fields[x - 1][y + 1].prevent_selection()

        for _ in range(size):
            if y != 0:
                self._fields[x][y - 1].prevent_selection()
            if y != 9:
                self._fields[x][y + 1].prevent_selection()

            self._fields[x][y].choose_field(str(size))
            x += 1

        if x != 10:
            if y != 0:
                self._fields[x][y - 1].prevent_selection()
            self._fields[x][y].prevent_selection()
            if y != 9:
                self._fields[x][y + 1].prevent_selection()

    def process_vertical(self, pair: Tuple[int, int], size: int) -> None:
        x, y = pair
        if y != 0:
            if x != 0:
                self._fields[x - 1][y - 1].prevent_selection()
            self._fields[x][y - 1].prevent_selection()
            if x != 9:
                self._fields[x + 1][y - 1].prevent_selection()

        for _ in range(size):
            if x != 0:
                self._fields[x - 1][y].prevent_selection()
            if x != 9:
                self._fields[x + 1][y].prevent_selection()

            self._fields[x][y].choose_field(str(size))
            y += 1

        if y != 10:
            if x != 0:
                self._fields[x - 1][y].prevent_selection()
            self._fields[x][y].prevent_selection()
            if x != 9:
                self._fields[x + 1][y].prevent_selection()

    def choose_fields(self, size: int, number_of_ships: int) -> None:
        counter = 0

        while counter < number_of_ships:
            horizontal_position = True if random.random() > 0.5 else False

            if horizontal_position:
                x = random.randint(0, 10 - size)
                y = random.randint(0, 9)

                if not self.can_ship_fit((x, y), size, horizontal=True):
                    continue

                self.process_horizontal((x, y), size)

            else:
                x = random.randint(0, 9)
                y = random.randint(0, 10 - size)

                if not self.can_ship_fit((x, y), size, horizontal=False):
                    continue

                self.process_vertical((x, y), size)
            counter += 1

    def choose_fields_for_computer_ships(self) -> None:
        # Named parameters to improve readability
        self.choose_fields(size=4, number_of_ships=1)
        self.choose_fields(size=3, number_of_ships=2)
        self.choose_fields(size=2, number_of_ships=3)
        self.choose_fields(size=1, number_of_ships=4)
