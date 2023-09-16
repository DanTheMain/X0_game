import random
import sys
from copy import deepcopy


from tictactoe.game_objects import PlayerType, PlayerMark, Player, GameGrid
from tictactoe.prints import MESSAGES, game_help

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


class Game:
    def __init__(self) -> None:
        self._default_choices = {str(s) for s in range(1, 10)}
        self._choices = deepcopy(self._default_choices)
        self._grid = GameGrid()
        self._player_marks = {PlayerMark.O, PlayerMark.X}
        self._user, self._bot = self._init_players()
        self._messages = MESSAGES

    def _init_players(self) -> tuple[Player, Player]:
        marks = list(self._player_marks)
        user = Player(PlayerType.USER, marks.pop(random.choice(range(2))))
        bot = Player(PlayerType.BOT, marks.pop())
        return user, bot

    def _handle_last_choice(self, message: str) -> None:
        print("\n".join([message, str(self._grid)]))
        self.exit_game()

    def _update_valid_choices(self, choice: str) -> None:
        if not self._choices:
            self._handle_last_choice(self._messages.draw)
        self._choices.remove(choice)

    def _get_player_choices(self, player: Player) -> list[int]:
        return [
            int(cell_number)
            for cell_number, cell_content in self._grid.grid_contents.items()
            if cell_content == player.MARK.value
        ]

    def _check_player_status(self, player: Player) -> None:
        choices = self._get_player_choices(player)
        for win in WIN_CONDITIONS:
            if set(win).issubset(set(choices)):
                self._handle_last_choice(self._messages.winner.format(player))

    def _handle_mark_choice(self, player: Player, choice: str) -> None:
        print(self._messages.choice.format(player, choice))
        self._grid.update(choice, player.MARK.value)
        print(self._grid)
        self._update_valid_choices(choice)
        self._check_player_status(player)

    def exit_game(self) -> None:
        print(self._messages.exit_game)
        sys.exit(0)

    def record_auto_choice(self) -> None:
        if not self._choices:
            self._handle_last_choice(self._messages.draw)
        self._handle_mark_choice(self._bot, random.choice(list(self._choices)))

    def record_user_choice(self, choice: str) -> bool:
        if choice not in self._choices:
            print(self._messages.unsupported_input.format(choice, self._choices))
            return False
        self._handle_mark_choice(self._user, choice)
        return True

    def get_user_input(self) -> str:
        return str(input(self._messages.user_prompt)).lower().strip()

    def play(self) -> None:
        choice = self.get_user_input()
        while choice not in QUIT_OPTIONS and self._choices:
            if choice in HELP_OPTIONS:
                print(
                    game_help(
                        str(self._grid),
                        GRID_DISPLAY_OPTIONS,
                        self._choices,
                        QUIT_OPTIONS,
                        self._user.MARK.value,
                        self._bot.MARK.value,
                    )
                )
            elif choice in GRID_DISPLAY_OPTIONS:
                print(self._grid)
            else:
                if self.record_user_choice(choice):
                    self.record_auto_choice()
            choice = self.get_user_input()
