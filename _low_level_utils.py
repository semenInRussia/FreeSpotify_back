from typing import Callable

_all_cash_function_manager = {}


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


class CashManagerCollection:
    def add_cash_function_manager(self, cash_function_manager: CashFunctionManager, func_name: str):
        if not self.get_cash_function_manager(func_name):
            _all_cash_function_manager[func_name] = cash_function_manager

    @staticmethod
    def get_cash_function_manager(func_name: str):
        return _all_cash_function_manager.get(func_name)


cash_manager_collection = CashManagerCollection()


def cashed_function(func):
    cash_manager_collection.add_cash_function_manager(
        CashFunctionManager(func), func.__class__.__name__
    )

    def new_func(*args, **kwargs):
        cash_function_manager = cash_manager_collection.get_cash_function_manager(func.__class__.__name__)

        return cash_function_manager.get(*args, **kwargs)

    return new_func


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
