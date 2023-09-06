# X0 game
import random
import sys

VALID_CHOICES = [str(s) for s in range(1,10)]
WIN_CONDITIONS = [[1,2,3], [4,5,6], [7,8,9], [1,4,7], [2,5,8], [3,6,9], [1,5,9], [3,5,7]]
CURRENT_GRID = {str(s): s for s in range(1,10)}
MARKS = ('X', '0')
USER_MARK, AUTO_MARK = None, None


def print_help() -> None:
    print('Game grid:')
    draw_current_grid()
    print(f'Currently valid choices: {VALID_CHOICES}')
    print('Type "g" to draw current game grid')
    print('Type "q" to quit')
    if USER_MARK is not None and AUTO_MARK is not None:
        print(f"User is playing as '{USER_MARK}', bot as '{AUTO_MARK}'")


def draw_current_grid():
    cg = CURRENT_GRID
    print(f"{cg['1']} | {cg['2']} | {cg['3']}")
    print(f"{cg['4']} | {cg['5']} | {cg['6']}")
    print(f"{cg['7']} | {cg['8']} | {cg['9']}")


def _handle_tie():
    print("no more valid moves left - it is a tie!")
    draw_current_grid()
    sys.exit(0)


def _handle_win(winner_mark: str):
    print(f"'{winner_mark}' is the winner!")
    draw_current_grid()
    sys.exit(0)


def _update_valid_choices(_choice: str):
    if not VALID_CHOICES:
        _handle_tie()
    VALID_CHOICES.remove(_choice)


def set_marks(marks: (int, int)):
    _i = random.choice([0,1])
    global USER_MARK, AUTO_MARK
    USER_MARK = marks[_i]
    AUTO_MARK = marks[not _i]


def _check_mark_game_status(mark: str):
    for win in WIN_CONDITIONS:
        if set(win).issubset(set([int(k) for k, v in CURRENT_GRID.items() if v == mark])):
            _handle_win(mark)


def update_grid(k, v):
    assert k in CURRENT_GRID, (f"specified cell '{k}' not in current grid, "
                               f"valid cells are {CURRENT_GRID.keys()}")
    assert v in MARKS, (f"specified value '{v}' invalid, "
                        f"valid values are {MARKS}")
    assert CURRENT_GRID[k] not in MARKS, (f"specified cell '{k}' "
                                          f"has already been chosen")
    CURRENT_GRID[k] = v
    _update_valid_choices(k)
    draw_current_grid()


def _handle_mark_choice(mark: str, _choice: str):
    print(f'"{mark}" choice: {_choice}')
    update_grid(_choice, mark)
    _check_mark_game_status(mark)


def record_auto_choice():
    if not VALID_CHOICES:
        _handle_tie()
    auto_choice = random.choice(VALID_CHOICES)
    _handle_mark_choice(AUTO_MARK, auto_choice)


def record_user_choice(user_choice: str) -> bool:
    if user_choice not in VALID_CHOICES:
        print(f'Unsupported input "{user_choice}", '
              f'valid values are {VALID_CHOICES}')
        return False
    _handle_mark_choice(USER_MARK, user_choice)
    return True


def get_user_input() -> str:
    return str(input()).lower()


def play_game():
    _choice = get_user_input()
    set_marks(MARKS)
    while _choice not in ('q', 'quit', 'exit') and VALID_CHOICES:
        if _choice in ('h', 'help'):
            print_help()
            _choice = get_user_input()
        elif _choice in ('g', 'show grid'):
            draw_current_grid()
            _choice = get_user_input()
        else:
            if record_user_choice(_choice):
                record_auto_choice()
            _choice = get_user_input()


if __name__ == '__main__':
    play_game()
