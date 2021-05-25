from my_request import humanized_link
from my_request import is_not_valid_page
from my_request import normalize_link


def test_humanized_link():
    link = "http://rocknation.su/upload/mp3/Kiss/1974%20-%20Hotter%20Than%20Hell/04.%20Hotter%20Than%20Hell.mp3"

    excepted = "http://rocknation.su/upload/mp3/Kiss/1974 - Hotter Than Hell/04. Hotter Than Hell.mp3"

    assert humanized_link(link) == excepted


def test_normalized_link():
    link = "http://rocknation.su/upload/mp3/Kiss/1974 - Hotter Than Hell/04. Hotter Than Hell.mp3"
    excepted = "http://rocknation.su/upload/mp3/Kiss/1974%20-%20Hotter%20Than%20Hell/04.%20Hotter%20Than%20Hell.mp3"

    assert normalize_link(link) == excepted


def test_is_not_valid_page():
    assert not is_not_valid_page("https://google.com")
    assert is_not_valid_page("https://kdkdjdeihfurhfebnvbrffbv.djedijefi.semIsCool")
