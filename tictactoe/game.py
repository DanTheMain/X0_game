import random
import sys
from enum import Enum, auto
from itertools import cycle


from tictactoe.game_objects import (
    PlayerType,
    PlayerMark,
    Player,
    User,
    Bot,
    GameGrid,
    Moves,
)

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


class GameResult(Enum):
    USER = auto()
    BOT = auto()
    DRAW = auto()


def print_game_result(game_result: GameResult) -> None:
    if game_result == GameResult.USER:
        print("you won!")
    elif game_result == GameResult.BOT:
        print("bot won")
    else:
        print("draw")


class Game:
    def __init__(self) -> None:
        self._grid = GameGrid()
        self._moves = Moves()
        self._user, self._bot = User(), Bot()
        self._init_player_marks()

    def _init_player_marks(self) -> None:
        marks = list({PlayerMark.O, PlayerMark.X})
        self._user.mark = marks.pop(random.choice(range(2)))
        self._bot.mark = marks.pop()

    def handle_last_move(self, game_result: GameResult) -> None:
        print_game_result(game_result)
        print(self._grid)
        self.exit_game()

    def update_moves(self, move: str) -> None:
        if not self._moves:
            self.handle_last_move(GameResult.DRAW)
        if not self._moves.remove(move):
            self.exit_game(f"bad player move {move} detected!")

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
                if player.ptype == PlayerType.USER:
                    self.handle_last_move(GameResult.USER)
                else:
                    self.handle_last_move(GameResult.BOT)

    def handle_player_move(self, player: Player, move: str) -> None:
        print(f'"{player}" choice: {move}')
        self._grid.update(move, player.mark)
        print(self._grid)
        self.update_moves(move)
        self._check_player_status(player)

    def exit_game(self, code: int | str = 0) -> None:
        print("Exiting game ...")
        sys.exit(code)

    def play(self) -> None:
        move = input(f"Enter any key to start game ({QUIT_OPTIONS} to quit): ")
        if move in QUIT_OPTIONS:
            self.exit_game()
        while self._moves:
            cycle(
                [
                    self.handle_player_move(
                        self._user, self._user.make_move(self._moves)
                    ),
                    self.handle_player_move(
                        self._bot, self._bot.make_move(self._moves)
                    ),
                ]
            )
