from dataclasses import dataclass
from enum import StrEnum


class GameGrid:
    def __init__(self) -> None:
        self._grid_contents: dict[str, str] = {str(s): str(s) for s in range(1, 10)}

    def __str__(self) -> str:
        grid = ""
        for cell_number, cell_content in self._grid_contents.items():
            grid = " | ".join(
                [grid, str(cell_content), "\n" if int(cell_number) % 3 == 0 else ""]
            )
        return grid

    @property
    def grid_contents(self) -> dict[str, str]:
        return self._grid_contents

    def update(self, cell_number: str, new_value: str) -> None:
        self._grid_contents[cell_number] = new_value


class PlayerMark(StrEnum):
    X = "X"
    O = "0"


class PlayerType(StrEnum):
    USER = "user"
    BOT = "bot"


@dataclass
class Player:
    PTYPE: PlayerType
    MARK: PlayerMark

    def __str__(self) -> str:
        return f"Player '{self.PTYPE.value}' ({self.MARK.value})"

    def make_move(self):
        raise NotImplementedError
