from brackets_lib import Brackets
from brackets_lib import add_brackets_around
from brackets_lib import delete_all_values_with_all_brackets_types


def test_delete_all_values_with_all_brackets_types():
    string = "(ldldldld)Hello, (dldldl)World!(ldldld)"
    assert delete_all_values_with_all_brackets_types(string) == "Hello, World!"


def test_delete_all_values_with_all_brackets_types_by_empty_string():
    string = ""
    assert delete_all_values_with_all_brackets_types(string) == ""


def test_add_brackets_around():
    assert add_brackets_around("str", Brackets("{", "}")) == "{str}"
