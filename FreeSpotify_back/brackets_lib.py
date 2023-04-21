from collections import namedtuple
from collections.abc import Iterable
from functools import reduce

Brackets = namedtuple("Brackets", ["open_char", "closed_char"])

ALL_BRACKETS_TYPES = [
    Brackets("(", ")"),
    Brackets("[", "]"),
]


def delete_all_values_with_all_brackets_types(string: str) -> str:
    return delete_all_values_with_given_brackets(string, ALL_BRACKETS_TYPES)


def delete_all_values_with_given_brackets(string: str,
                                          brackets_types: Iterable[Brackets],
                                          ) -> str:
    for brackets in brackets_types:
        string = delete_value_with_brackets_pair(string, brackets)
    return string


def delete_value_with_brackets_pair(string: str, brackets: Brackets) -> str:
    inside_brackets = get_values_with_brackets(string, brackets)
    return reduce(
        lambda old, inside_brackets: old.replace(inside_brackets, ""),
        inside_brackets,
        string,
    )


def ignore_brackets_around(string: str) -> str:
    """Return the modified string without brackets around.

    String should has 2 brackets: first at the string start, second at the
    string end
    """
    return string[1:-1]


def get_values_with_brackets(string: str, brackets: Brackets) -> Iterable[str]:
    while _is_string_has_brackets(string, brackets):
        inside_brackets = _find_one_value_inside_brackets(string, brackets)
        yield inside_brackets
        string = string.replace(inside_brackets, "")

def get_values_inside_of_brackets(string: str, brackets: Brackets) -> Iterable[str]:
    return map(ignore_brackets_around, get_values_with_brackets(string, brackets))


def _find_one_value_inside_brackets(string: str, brackets: Brackets) -> str:
    open_branch_index = string.find(brackets.open_char)
    closed_branch_index = string.find(brackets.closed_char) + 1
    return string[open_branch_index: closed_branch_index]


def _is_string_has_brackets(string: str, brackets: Brackets) -> bool:
    return (brackets.open_char in string) and (brackets.closed_char in string)


def add_brackets_around(string: str, brackets: Brackets) -> str:
    return brackets.open_char + string + brackets.closed_char
