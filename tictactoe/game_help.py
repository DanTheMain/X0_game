from typing import Iterable


def _format_item(template: str, options: str | Iterable[str], sep: str) -> str:
    return template.format(
        f"{sep}".join(options) if isinstance(options, (tuple, list)) else options
    )


def game_help(
    grid: str,
    moves: set[str],
    quit_options: Iterable[str],
    user_mark: str,
    bot_mark: str,
) -> str:

    return "\n".join(
        [
            _format_item("{}", ("Help.", "Game grid: ", f"{grid}"), "\n"),
            _format_item("Currently valid choices: {}", moves, ", "),
            _format_item("Type {} to quit the game", quit_options, " or "),
            f"User mark: '{user_mark}', bot mark: '{bot_mark}'",
        ]
    )
