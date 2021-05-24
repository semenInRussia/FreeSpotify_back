from collections import namedtuple
from functools import reduce
from typing import List

Brackets = namedtuple("Brackets", ["open_char", "closed_char"])


def delete_all_values_with_all_brackets(string: str):
    brackets_types = [
        Brackets("(", ")"),
        Brackets("[", "]")
    ]

    return delete_all_values_with_many_brackets(string, brackets_types)


def delete_all_values_with_many_brackets(string: str, brackets_types: List[Brackets]) -> str:
    for brackets in brackets_types:
        string = delete_value_in_brackets(string, brackets)

    return string


def delete_value_in_brackets(string: str, brackets: Brackets) -> str:
    values_with_brackets = get_values_with_brackets(string, brackets)
    old_string_and_values_with_brackets = [string, *values_with_brackets]

    return reduce(
        lambda old_string, value_with_brackets: old_string.replace(value_with_brackets, ""),
        old_string_and_values_with_brackets
    )


def get_insides_of_brackets(string: str, brackets: Brackets) -> List[str]:
    return list(map(
        get_one_inside_of_brackets,
        get_values_with_brackets(string, brackets)
    ))


def get_one_inside_of_brackets(string: str) -> str:
    return string[1:-1]


def get_values_with_brackets(string: str, brackets: Brackets) -> List[str]:
    values_with_brackets = []

    while _is_string_has_brackets(string, brackets):
        value_with_brackets = _get_one_value_with_brackets_from_string(string, brackets)
        values_with_brackets.append(value_with_brackets)
        string = string.replace(value_with_brackets, "")

    return values_with_brackets


def _get_one_value_with_brackets_from_string(string: str, brackets: Brackets) -> str:
    open_branch_index = string.find(brackets.open_char)
    closed_branch_index = string.find(brackets.closed_char) + 1

    value_with_brackets = string[open_branch_index: closed_branch_index]

    return value_with_brackets


def _is_string_has_brackets(string: str, brackets: Brackets) -> bool:
    return brackets.open_char in string and brackets.closed_char


def add_brackets(string: str, brackets: Brackets) -> str:
    return brackets.open_char + string + brackets.closed_char
