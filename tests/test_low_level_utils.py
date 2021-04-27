from unittest.mock import MagicMock
from unittest.mock import create_autospec

import pytest

from _low_level_utils import CashFunctionManager
from _low_level_utils import cashed_function
from _low_level_utils import get_public_fields_of
from _low_level_utils import sum_of_lists


class TestClass:
    def __init__(self):
        pass

    def __eq__(self, other):
        pass

    _private_field1 = None
    _private_field2 = None

    public_field = None
    protected_field = None


@pytest.fixture()
def function():
    _handler = lambda *args, **kwargs: None

    return create_autospec(_handler, return_value=5)


def test_sum_of_lists():
    assert sum_of_lists([1, 2]) == [1, 2]
    assert sum_of_lists([1, 2], [3, 4]) == [1, 2, 3, 4]

    assert sum_of_lists(["str1", "str2"]) == ["str1", "str2"]

    assert sum_of_lists(*[['dir\\subdir1', 'dir\\subdir2']]) == ['dir\\subdir1', 'dir\\subdir2']


def test_get_public_fields_of():
    assert get_public_fields_of(TestClass, ignore=["protected_field"]) == ["public_field"]


def test_cash_function_manager(function: MagicMock):
    cash_manager = CashFunctionManager(function)

    assert cash_manager.get(
        (1, (("name", "SEMEN"),))
    ) == 5

    assert cash_manager.get(
        (1, (("name", "SEMEN"),))
    ) == 5

    function.assert_called_once_with(1, name="SEMEN")


def test_cashed_function(function):
    mock_cashed_function = cashed_function(function)

    mock_cashed_function(1)
    mock_cashed_function(1)
    mock_cashed_function(1)

    function.assert_called_once()
