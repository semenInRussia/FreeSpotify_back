from unittest.mock import MagicMock, create_autospec

import pytest
from FreeSpotify_back._low_level_utils import (
    cached_function,
    first_true,
    get_public_fields_of,
    my_format_str,
)


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
    _func = lambda *args, **kwargs: None
    return create_autospec(_func, return_value=5)


@pytest.fixture()
def function2():
    _func = lambda *args, **kwargs: None
    return create_autospec(_func, return_value=5)


def test_get_public_fields_of():
    assert get_public_fields_of(TestClass,
                                ignore_list=["protected_field"]) == ["public_field"]


def test_cached_function(function: MagicMock):
    current_cached_function = cached_function(function)

    assert current_cached_function(1, name="SEMEN") == 5
    assert current_cached_function(1, name="SEMEN") == 5

    function.assert_called_once_with(1, name="SEMEN")


def test_my_format_str():
    assert my_format_str("{} {}", 1, 1) == "1 1"


def test_my_format_str_by_kwargs():
    assert my_format_str("{name}!", name="semen") == "semen!"


def test_my_format_with_expression():
    assert my_format_str("{1 + 2}") == "3"


def test_my_format_with_expression_with_spaces():
    assert my_format_str("{ 1 + 2 }") == "3"


def test_my_format_with_expression_with_funcs_from_kwargs():
    assert my_format_str("{f([1, 3])}", f=sum) == "4"


def test_my_format_with_or():
    assert my_format_str("my {last_name|first_name}", last_name="Bond", first_name="James") == "my Bond"
    assert my_format_str("my {last_name|first_name}", last_name=None, first_name="James") == "my James"

def test_first_true():
    assert first_true(["", False, "Value", "Anotther Value"]) == "Value"
    assert first_true(["Moscow", "St. Petersburg", "Ekaterinburg"],
                      pred=lambda c: len(c.split()) > 1,
                      default="Veliky Luki") == "St. Petersburg"
    assert first_true(["Moscow", "Volgograd", "Ekaterinburg"],
                      pred=lambda c: len(c.split()) > 1,
                      default="Veliky Luki") == "Veliky Luki"
