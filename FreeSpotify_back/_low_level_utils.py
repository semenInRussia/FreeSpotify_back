from collections.abc import Iterable
from functools import lru_cache
from typing import Callable, Optional

from typing_extensions import TypeVar

from .brackets_lib import Brackets, add_brackets_around, get_values_inside_of_brackets
from .core.exceptions import InvalidFormatExpressionError

cached_function = lru_cache()

format_brackets = Brackets("{", "}")
or_char = "|"


def format_exception(error: Exception) -> str:
    error_name = error.__class__.__name__
    error_description = error.__doc__

    if error_description:
        error_description = f'Description - "{error_description}"'
    else:
        error_description = "Description not found..."

    return (
        "Sorry... I'm found error...\n"
        "Detail:\n"
        f"|     Name - {error_name}\n"
        f"|     {error_description}"
    )


def get_public_fields_of(obj,
                         ignore_list: Optional[list[str]] = None) -> list[str]:
    if ignore_list is None:
        ignore_list = []
    all_fields = dir(obj)

    return list(filter(lambda f: _is_public_field_name(f, ignore_list),
                       all_fields))

def _is_public_field_name(field_name: str,
                          ignore_list: Optional[list[str]]=None) -> bool:
    if ignore_list is None:
        ignore_list = []
    return not (field_name.startswith("_") or field_name in ignore_list)

def my_format_str(string: str, *args, **kwargs) -> str:
    insides_of_brackets = get_values_inside_of_brackets(string, format_brackets)

    for inside_of_brackets in insides_of_brackets:
        current_expression = _get_format_expression(inside_of_brackets, args, kwargs)

        old_string = add_brackets_around(inside_of_brackets, format_brackets)
        new_string = str(current_expression.execute())

        string = string.replace(old_string, new_string)

        args = current_expression.args
        kwargs = current_expression.kwargs

    return string


class FormatExpression:
    def __init__(self, str_expression: str, args: tuple, kwargs: dict):
        self._str_expression = str_expression
        self._args = args
        self._kwargs = kwargs

    @staticmethod
    def is_this_expression(_str_expression: str) -> bool:
        return NotImplemented

    def execute(self) -> str:
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
        return not str_expression.strip()

    def execute(self) -> str:
        res = self._args[0]
        self._args = self._args[1:]
        return res


class OrFormatExpression(FormatExpression):
    @staticmethod
    def is_this_expression(str_expression: str) -> bool:
        return or_char in str_expression

    def execute(self) -> str:
        parts_of_expression = self._str_expression.split(or_char)
        if self._is_valid_expression(parts_of_expression[0]):
            return eval(parts_of_expression[0], self.kwargs)
        return eval(parts_of_expression[1], self.kwargs)

    def _is_valid_expression(self, expression: str) -> bool:
        try:
            result = eval(expression, self.kwargs)
        except:
            return False
        else:
            return bool(result)


class DefaultFormatExpression(FormatExpression):
    @staticmethod
    def is_this_expression(_str_expression: str) -> bool:
        return True

    def execute(self) -> str:
        return eval(self._str_expression, self.kwargs)


def _get_format_expression(expression: str,
                           args: tuple,
                           kwargs: dict) -> FormatExpression:
    for format_expression in all_format_expression:
        if format_expression.is_this_expression(expression):
            return format_expression(expression, args, kwargs)
    raise InvalidFormatExpressionError


all_format_expression: list[type[FormatExpression]] = [
    EmptyFormatExpression,
    OrFormatExpression,
    DefaultFormatExpression]


Element = TypeVar("Element")

# code taked from the itertools recipes
def first_true(iterable: Iterable[Element],
               default: Optional[Element] = None,
               pred: Optional[Callable[[Element], bool]] = None) -> Optional[Element]:
    """Return the first true value in the iterable.

    If no true value is found, returns *default*

    If *pred* is not None, returns the first item
    for which pred(item) is true.
    """
    # first_true([a,b,c], x) --> a or b or c or x
    # first_true([a,b], x, f) --> a if f(a) else b if f(b) else x
    return next(filter(pred, iterable), default)
