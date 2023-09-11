import random
import sys
from copy import deepcopy

from game_objects import PlayerType, PlayerMark, Player, GameGrid


class Game:
    def __init__(self) -> None:
        self._win_conditions = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9],
            [1, 4, 7],
            [2, 5, 8],
            [3, 6, 9],
            [1, 5, 9],
            [3, 5, 7],
        ]

        self._quit_options = ("q", "quit", "x", "exit")
        self._help_options = ("h", "help")
        self._grid_display_options = ("g", "grid")

        self._default_choices = [str(s) for s in range(1, 10)]
        self._choices = deepcopy(self._default_choices)

        self._grid = GameGrid()

        self._user, self._bot = self._init_players()

    @staticmethod
    def _init_players() -> tuple[Player, Player]:
        marks = [PlayerMark.O, PlayerMark.X]
        return Player(PlayerType.user, marks.pop(random.choice(range(1)))), Player(
            PlayerType.bot, marks[0]
        )

    def _handle_last_choice(self, message: str | None) -> None:
        print("\n".join([message or "", str(self._grid)]))
        self.exit_game()

    def _update_valid_choices(self, choice: str) -> None:
        if not self._choices:
            self._handle_last_choice("no more valid moves left - it is a draw!")
        self._choices.remove(choice)

    def _check_player_status(self, player: Player) -> None:
        mark_choices = [
            int(k)
            for k, v in self._grid.grid_contents.items()
            if v == player.mark.value
        ]
        for win in self._win_conditions:
            if set(win).issubset(set(mark_choices)):
                self._handle_last_choice(f"{player} is the winner!")

    def _handle_mark_choice(self, player: Player, choice: str) -> None:
        print(f'"{player}" choice: {choice}')
        self._grid.update(choice, player.mark.value, True)
        self._update_valid_choices(choice)
        self._check_player_status(player)

    @staticmethod
    def _format_help_choice_item(
        template: str, options: str | tuple[str, ...] | list[str], sep: str
    ) -> str:
        options = (
            f"{sep}".join(options) if isinstance(options, (tuple, list)) else options
        )
        return template.format(options)

    @staticmethod
    def exit_game(exit_details: int | str = 0) -> None:
        sys.exit(exit_details)

    def get_help(self) -> None:
        print("\n".join(["Help contents:", "Game grid:", f"{str(self._grid)}"]))
        print(
            self._format_help_choice_item(
                "Currently valid choices: {}", self._choices, ", "
            )
        )
        print(
            self._format_help_choice_item(
                "Type {} to draw current game grid", self._grid_display_options, " or "
            )
        )
        print(
            self._format_help_choice_item(
                "Type {} to quit the game", self._quit_options, " or "
            )
        )
        print(
            f"User mark: '{self._user.mark.value}', bot mark: '{self._bot.mark.value}'"
        )

    def record_auto_choice(self, custom_choice: str | None = None) -> None:
        if not self._choices:
            self._handle_last_choice("no more valid moves left - it is a draw!")
        self._handle_mark_choice(
            self._bot, custom_choice or random.choice(self._choices)
        )

    def record_user_choice(self, choice: str) -> bool:
        if choice not in self._choices:
            print(f'Unsupported input "{choice}", valid values are {self._choices}')
            return False
        self._handle_mark_choice(self._user, choice)
        return True

    @staticmethod
    def get_user_input(user_prompt: str = "Enter your choice: ") -> str:
        return str(input(user_prompt)).lower().strip()

    def play(self) -> None:
        choice = self.get_user_input()
        while choice not in self._quit_options and self._choices:
            if choice in self._help_options:
                self.get_help()
            elif choice in self._grid_display_options:
                print(self._grid)
            else:
                if self.record_user_choice(choice):
                    self.record_auto_choice()
            choice = self.get_user_input()

