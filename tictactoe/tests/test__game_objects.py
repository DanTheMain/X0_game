from copy import deepcopy
from pytest import raises
from tictactoe.game_objects import DEFAULT_GRID, GameGrid


def test__game_grid_initialization():
    gg = GameGrid()

    assert gg is not None and gg.grid_contents == DEFAULT_GRID


def test__game_grid__string_representation():
    expected_str = ' | 1 |  | 2 |  | 3 | \n | 4 |  | 5 |  | 6 | \n | 7 |  | 8 |  | 9 | \n'

    assert str(GameGrid()) == expected_str


def test__game_grid__updated_string_representation():
    gg = GameGrid()
    gg._grid_contents['1'], gg._grid_contents['8'] = 'X', 'O'
    expected_str = ' | X |  | 2 |  | 3 | \n | 4 |  | 5 |  | 6 | \n | 7 |  | O |  | 9 | \n'

    assert str(gg) == expected_str



def test__game_grid__contents_property():
    gg = GameGrid()

    assert gg.grid_contents == DEFAULT_GRID


def test__game_grid__update_with_valid_value():
    gg = GameGrid()
    gg.update('4', 'NEW')
    expected = deepcopy(DEFAULT_GRID)
    expected.update({'4': 'NEW'})

    assert gg.grid_contents == expected


def test__game_grid__update_with_invalid_value():
    with raises(ValueError):
        GameGrid().update('10', 'NEW')
