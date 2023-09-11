from dataclasses import dataclass
from enum import Enum


class GameGrid:
    def __init__(self) -> None:
        self._grid_contents: dict[str, str] = {str(s): str(s) for s in range(1, 10)}

    def __str__(self) -> str:
        s = ""
        for k, v in self._grid_contents.items():
            s = " | ".join([s, str(v), "\n" if int(k) % 3 == 0 else ""])
        return s

    @property
    def grid_contents(self) -> dict[str, str]:
        return self._grid_contents

    def update(self, k: str, v: str, should_print: bool = False) -> None:
        self._grid_contents[k] = v
        if should_print:
            print(str(self))


class PlayerMark(Enum):
    X: str = "X"
    O: str = "0"


class PlayerType(Enum):
    user: str = "user"
    bot: str = "bot"


@dataclass
class Player:
    ptype: PlayerType
    mark: PlayerMark

    def __str__(self) -> str:
        return f"Player '{self.ptype.value}' ({self.mark.value})"

