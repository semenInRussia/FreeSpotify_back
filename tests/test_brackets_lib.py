from brackets_lib import Brackets
from brackets_lib import add_brackets
from brackets_lib import delete_all_values_with_all_brackets
from brackets_lib import get_insides_of_brackets
from brackets_lib import get_one_inside_of_brackets
from brackets_lib import get_values_with_brackets


def test_delete_all_values_with_all_brackets():
    string = "(ldldldld)Hello, (dldldl)World!(ldldld)"

    assert delete_all_values_with_all_brackets(string) == "Hello, World!"


def test_delete_all_values_with_all_brackets_by_empty_string():
    string = ""

    assert delete_all_values_with_all_brackets(string) == ""


def test_get_values_with_brackets():
    string = "(in)Hello,(in2)World!(in3)"

    assert get_values_with_brackets(string, Brackets("(", ")")) == ["(in)", "(in2)", "(in3)"]


def test_get_insides_of_brackets():
    string = "(in)Hello,(in2)World!(in3)"

    assert get_insides_of_brackets(string, Brackets("(", ")")) == ["in", "in2", "in3"]


def test_get_one_inside_of_brackets():
    assert get_one_inside_of_brackets("(str)") == "str"


def test_add_brackets():
    assert add_brackets("str", Brackets("{", "}")) == "{str}"
