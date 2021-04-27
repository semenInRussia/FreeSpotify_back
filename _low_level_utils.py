from typing import Callable


def sum_of_lists(*lists):
    result = []

    for current_list in lists:
        result.extend(current_list)

    return result


def get_public_fields_of(obj, ignore=None):
    if ignore is None:
        ignore = []

    all_fields = dir(obj)
    is_public_field_name = lambda field_name: not (field_name.startswith("_") or field_name in ignore)

    return list(filter(
        is_public_field_name,

        all_fields
    ))


class CashFunctionManager:
    _cashed_values = {}
    _func: Callable

    def __init__(self, function: Callable):
        self._func = function

    def get(self, key):
        if self._cashed_values.get(key):
            return self._cashed_values[key]
        else:
            result = self._func(key)

            self.set(key, result)

            return result

    def set(self, key, value):
        self._cashed_values[key] = value
