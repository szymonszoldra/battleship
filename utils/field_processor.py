import random
from components.field import Field


class FieldProcessor:
    def __init__(self, computer_fields: list[list[Field]]) -> None:
        self._computer_fields = computer_fields

    def choose_fields_for_size_4(self) -> None:
        horizontal_position = True if random.random() > 0.5 else False

        if horizontal_position:
            # starting coords
            x = random.randint(0, 6)
            y = random.randint(0, 9)

            if x != 0:
                if y != 0:
                    self._computer_fields[x - 1][y - 1].prevent_selection()
                self._computer_fields[x - 1][y].prevent_selection()
                if y != 9:
                    self._computer_fields[x - 1][y + 1].prevent_selection()

            for _ in range(4):
                if y != 0:
                    self._computer_fields[x][y - 1].prevent_selection()
                if y != 9:
                    self._computer_fields[x][y + 1].prevent_selection()

                self._computer_fields[x][y].choose_field()
                x += 1

            if x != 10:
                if y != 0:
                    self._computer_fields[x][y - 1].prevent_selection()
                self._computer_fields[x][y].prevent_selection()
                if y != 9:
                    self._computer_fields[x][y + 1].prevent_selection()

        else:
            # starting coords
            x = random.randint(0, 9)
            y = random.randint(0, 6)

            if y != 0:
                if x != 0:
                    self._computer_fields[x - 1][y - 1].prevent_selection()
                self._computer_fields[x][y - 1].prevent_selection()
                if x != 9:
                    self._computer_fields[x + 1][y - 1].prevent_selection()

            for _ in range(4):
                if x != 0:
                    self._computer_fields[x - 1][y].prevent_selection()
                if x != 9:
                    self._computer_fields[x + 1][y].prevent_selection()

                self._computer_fields[x][y].choose_field()
                y += 1

            if y != 10:
                if x != 0:
                    self._computer_fields[x - 1][y].prevent_selection()
                self._computer_fields[x][y].prevent_selection()
                if x != 9:
                    self._computer_fields[x + 1][y].prevent_selection()

    def choose_fields_for_computer_ships(self) -> None:
        self.choose_fields_for_size_4()
