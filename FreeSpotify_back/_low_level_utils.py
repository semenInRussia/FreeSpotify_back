from functools import lru_cache
from typing import List

from .brackets_lib import Brackets
from .brackets_lib import add_brackets_around
from .brackets_lib import get_values_inside_of_brackets

cached_function = lru_cache()

format_brackets = Brackets("{", "}")
or_char = "|"


def format_exception(error: Exception) -> str:
    error_name = error.__class__.__name__
    error_description = error.__doc__

    if error_description:
        error_description = f"Description - \"{error_description}\""
    else:
        error_description = "Description not found..."

    return (
        f"Sorry... I'm found error...\n"
        "Detail:\n"
        f"|     Name - {error_name}\n"
        f"|     {error_description}"
    )


def get_public_fields_of(obj, ignore=None):
    if ignore is None:
        ignore = []

    all_fields = dir(obj)
    is_public_field_name = lambda field_name: not (field_name.startswith("_") or field_name in ignore)

    return list(filter(is_public_field_name, all_fields))


def my_format_str(string: str, *args, **kwargs) -> str:
    insides_of_brackets = get_values_inside_of_brackets(string, format_brackets)

    for inside_of_brackets in insides_of_brackets:
        current_expression = _get_format_expression(inside_of_brackets, args, kwargs)

        old_string = add_brackets_around(inside_of_brackets, format_brackets)
        new_string = str(current_expression.execute())

        string = string.replace(
            old_string,
            new_string
        )

        args = current_expression.args
        kwargs = current_expression.kwargs

    return string


class FormatExpression:
    def __init__(self, str_expression: str, args: tuple, kwargs: dict):
        self._str_expression = str_expression
        self._args = args
        self._kwargs = kwargs

    @staticmethod
    def is_this_expression(str_expression: str) -> bool:
        pass

    def execute(self):
        pass

    @property
    def args(self) -> tuple:
        return self._args

    @property
    def kwargs(self) -> dict:
        return self._kwargs


class EmptyFormatExpression(FormatExpression):
    @staticmethod
    def is_this_expression(str_expression: str) -> bool:
        return str_expression.strip() == ''

    def execute(self):
        res = self._args[0]
        self._args = self._args[1:]
        return res


class OrFormatExpression(FormatExpression):
    @staticmethod
    def is_this_expression(str_expression: str) -> bool:
        return or_char in str_expression

    def execute(self):
        parts_of_expression = self._str_expression.split(or_char)
        if self._is_valid_expression(parts_of_expression[0]):
            return eval(parts_of_expression[0], self.kwargs)
        else:
            return eval(parts_of_expression[1], self.kwargs)

    def _is_valid_expression(self, expression) -> bool:
        try:
            result = eval(expression, self.kwargs)
        except:
            return False
        else:
            return bool(result)


class DefaultFormatExpression(FormatExpression):
    @staticmethod
    def is_this_expression(str_expression: str) -> bool:
        return True

    def execute(self):
        return eval(self._str_expression, self.kwargs)


def _get_format_expression(expression: str, args: tuple, kwargs: dict):
    for format_expression in all_format_expression:
        if format_expression.is_this_expression(expression):
            return format_expression(expression, args, kwargs)


all_format_expression: List[type[FormatExpression]] = [
    EmptyFormatExpression,
    OrFormatExpression,
    DefaultFormatExpression
]


# code taked from the itertools recipes
def first_true(iterable, default=False, pred=None):
    """Returns the first true value in the iterable.

    If no true value is found, returns *default*

    If *pred* is not None, returns the first item
    for which pred(item) is true.
    """
    # first_true([a,b,c], x) --> a or b or c or x
    # first_true([a,b], x, f) --> a if f(a) else b if f(b) else x
    return next(filter(pred, iterable), default)
