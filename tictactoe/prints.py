from enum import StrEnum
from typing import Iterable


class MESSAGES(StrEnum):
    user_prompt = "Enter your choice: "
    choice = '"{}" choice: {}'
    exit_game = "Exiting game ..."
    draw = "no more valid moves left - it is a draw!"
    unsupported_input = 'Unsupported input "{}", valid values are {}'
    winner = "{} is the winner!"


def game_help(
    grid: str,
    grid_options: Iterable[str],
    choices: set[str],
    quit_options: Iterable[str],
    user_mark: str,
    bot_mark: str,
) -> str:
    def format_item(template: str, options: str | Iterable[str], sep: str) -> str:
        return template.format(
            f"{sep}".join(options) if isinstance(options, (tuple, list)) else options
        )

    return "\n".join(
        [
            format_item("{}", ("Help.", "Game grid: ", f"{grid}"), "\n"),
            format_item("Currently valid choices: {}", choices, ", "),
            format_item("Type {} for game grid", grid_options, " or "),
            format_item("Type {} to quit the game", quit_options, " or "),
            f"User mark: '{user_mark}', bot mark: '{bot_mark}'",
        ]
    )
