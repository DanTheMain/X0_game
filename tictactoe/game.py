from copy import deepcopy
from itertools import cycle
import random
from typing import Optional
import sys

from tictactoe.game_help import game_help

from tictactoe.game_objects import (
    PlayerMark,
    Player,
    User,
    Bot,
    GameGrid,
)

DEFAULT_CHOICES = {str(s) for s in range(1, 10)}
WIN_CONDITIONS = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],
    [1, 4, 7],
    [2, 5, 8],
    [3, 6, 9],
    [1, 5, 9],
    [3, 5, 7],
]


QUIT_OPTIONS = ("q", "quit", "x", "exit")
HELP_OPTIONS = ("h", "help")
GRID_DISPLAY_OPTIONS = ("g", "grid")


def print_game_result(winner: Optional[Player]) -> None:
    if winner is None:
        print("draw")
    else:
        print(f"{winner} won")


class Game:
    def __init__(self) -> None:
        self._name = "tictactoe"
        self._grid = GameGrid()
        self._moves = deepcopy(DEFAULT_CHOICES)
        self._user, self._bot = User(), Bot()
        self._init_player_marks()
        self.players = (self._user, self._bot)

    def _init_player_marks(self) -> None:
        marks: list[PlayerMark] = [PlayerMark.X, PlayerMark.O]
        self._user.mark = marks.pop(random.choice(range(2)))
        self._bot.mark = marks.pop()

    def handle_last_move(self, winner: Player | None) -> None:
        print_game_result(winner)
        print(self._grid)
        self.exit_game()

    def update_moves(self, move: str) -> None:
        if not self._moves:
            self.handle_last_move(winner=None)
        self._moves.remove(move)

    def _get_player_choices(self, player: Player) -> list[int]:
        return [
            int(cell_number)
            for cell_number, cell_content in self._grid.grid_contents.items()
            if cell_content == player.mark.value
        ]

    def _check_player_status(self, player: Player) -> None:
        choices = self._get_player_choices(player)
        for win in WIN_CONDITIONS:
            if set(win).issubset(set(choices)):
                self.handle_last_move(player)

    def handle_player_move(self, player: Player) -> None:
        if not self._moves:
            raise RuntimeError(f"Game {self._name} ran out of moves!")
        move = player.make_move(self._moves)
        print(f'"{player}" choice: {move}')
        self._grid.update(move, player.mark)
        print(self._grid)
        self.update_moves(move)
        self._check_player_status(player)

    def exit_game(self, code: int | str = 0) -> None:
        print("Exiting game ...")
        sys.exit(code)

    def play(self) -> None:
        print(
            game_help(
                str(self._grid),
                list(self._moves),
                list(QUIT_OPTIONS),
                self._user.mark,
                self._bot.mark,
            )
        )
        if (
            input(f"Enter any key to start game ({QUIT_OPTIONS} to quit): ")
            in QUIT_OPTIONS
        ):
            self.exit_game()
        for player in cycle(self.players):
            self.handle_player_move(player)
