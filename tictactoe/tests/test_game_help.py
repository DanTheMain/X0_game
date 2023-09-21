from tictactoe.game_help import _format_item, game_help


def test__format_item__with_string_type_option_returned_substituted() -> None:
    template, options = "template ", "options"
    assert _format_item(template + "{}", options, ", ") == template + options


def test__format_item__with_list_type_option_returned_formatted_substituted() -> None:
    template, options, sep = "{}", list("options"), ","
    assert _format_item(template, options, sep) == sep.join(options)


def test__format_item__with_tuple_type_option_returned_formatted_substituted() -> None:
    template, options, sep = "{}", tuple(list("options")), ","
    assert _format_item(template, options, sep) == sep.join(options)


def test__format_item__with_worded_template_returns_substituted() -> None:
    before_template, after_template = "before ", " after"
    template, options, sep = before_template + "{}" + after_template, "options", ","
    assert (
        _format_item(template, options, sep)
        == before_template + options + after_template
    )


def test__game_help() -> None:
    expected = (
        "Help.\nGame grid: \ngrid\nCurrently valid choices: m, o, v, e, s\nType q or u or i or t to quit the game\n"
        + "User mark: 'user', bot mark: 'bot'"
    )
    assert game_help("grid", list("moves"), list("quit"), "user", "bot") == expected
