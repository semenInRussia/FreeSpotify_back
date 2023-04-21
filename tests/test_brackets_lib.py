from FreeSpotify_back.brackets_lib import (
    Brackets,
    add_brackets_around,
    delete_all_values_with_all_brackets_types,
)


def test_delete_all_values_with_all_brackets_types():
    string = "(ldldldld)Hello, (dldldl)World!(ldldld)"
    assert delete_all_values_with_all_brackets_types(string) == "Hello, World!"


def test_delete_all_values_with_all_brackets_types_by_empty_string():
    string = ""
    assert delete_all_values_with_all_brackets_types(string) == ""


def test_add_brackets_around():
    assert add_brackets_around("str", Brackets("{", "}")) == "{str}"
