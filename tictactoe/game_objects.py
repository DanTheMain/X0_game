from enum import StrEnum
from copy import deepcopy
from random import choice


DEFAULT_GRID = {str(s): str(s) for s in range(1, 10)}
DEFAULT_CHOICES = {str(s) for s in range(1, 10)}


class Moves:
    def __init__(self) -> None:
        self._moves: set[str] = deepcopy(DEFAULT_CHOICES)

    def __str__(self) -> str:
        return ", ".join([c for c in self._moves])

    def get(self) -> set[str]:
        return self._moves

    def is_valid(self) -> bool:
        return self._moves is not None and len(self._moves) > 0

    def is_valid_move(self, p_move: str) -> bool:
        return p_move in self._moves

    def remove(self, move: str) -> bool:
        if self.is_valid() and self.is_valid_move(move):
            self._moves.remove(move)
            return True
        return False


class GameGrid:
    def __init__(self) -> None:
        self._grid_contents: dict[str, str] = deepcopy(DEFAULT_GRID)

    def __str__(self) -> str:
        grid = ""
        for cell_number, cell_content in self._grid_contents.items():
            grid = " | ".join(
                [grid, str(cell_content), "\n" if int(cell_number) % 3 == 0 else ""]
            )
        return grid

    def __repr__(self) -> str:
        return str(self._grid_contents.items())

    @property
    def grid_contents(self) -> dict[str, str]:
        return self._grid_contents

    def update(self, cell_number: str, new_value: str) -> None:
        if cell_number in self.grid_contents:
            self._grid_contents[cell_number] = new_value


class PlayerMark(StrEnum):
    X = "X"
    O = "0"


class PlayerType(StrEnum):
    USER = "user"
    BOT = "bot"


class Player:
    ptype: PlayerType = None
    mark: PlayerMark = None

    def __init__(self) -> None:
        pass

    def __str__(self) -> str:
        return f"Player '{self.ptype.value}' ({self.mark.value})"

    def make_move(self, moves: Moves) -> None:
        raise NotImplementedError


def is_valid_move(move: str, valid_moves: Moves) -> bool:
    if move not in valid_moves.get():
        print(f'Unsupported move "{move}", valid values are {valid_moves}')
        return False
    return True


def get_input(prompt):
    return str(input(prompt).lower().strip())


class User(Player):
    def __init__(self):
        super().__init__()
        self.ptype = PlayerType.USER

    def make_move(self, moves: Moves) -> str | None:
        if not moves.is_valid():
            return None
        move = get_input("Enter your choice: ")
        while not moves.is_valid_move(move):
            move = get_input(f"Invalid choice '{move}' - please make another: ")
        return move


class Bot(Player):
    def __init__(self):
        super().__init__()
        self.ptype = PlayerType.BOT

    def make_move(self, moves: Moves) -> str | None:
        return choice(list(moves.get())) if moves.is_valid() else None
