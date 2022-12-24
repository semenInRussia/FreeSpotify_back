from FreeSpotify_back import similarity_lib

test_strings = ["a", "ac dc", "b", "AC/DC", "AC/dc"]


def test_search_string_similar_to():
    actual = similarity_lib.search_string_similar_to("acdc",
        ["metallica", "Black Sabbath", "AC/DC"])

    assert actual == "AC/DC"

def test_filter_and_sort_strings_by_min_similarity_to():
    actual = list(similarity_lib.filter_and_sort_strings_by_min_similarity_to(
        "AC/DC",
        ["a", "ac dc", "b", "AC/DC", "AC/dc"]))

    assert actual == ["AC/DC", "AC/dc", "ac dc"]


def test_filter_objects_by_min_similarity_to():
    actual = list(similarity_lib.filter_objects_by_min_similarity_to(
        "AC/DC", ["b", "jrfihguthrgtgitjht", "kdkoooo", "ac dc"]))

    assert actual == ["ac dc"]


def test_sort_objects_by_similarity_to():
    actual = list(similarity_lib.
        sort_objects_by_similarity_to("AC/DC",
                                      ["AC DC", "AC/DC", "ac dc", "a", "acdc"]))

    assert actual == ['AC/DC', 'acdc', 'AC DC', 'ac dc', 'a']


def test_is_similar_strings():
    assert similarity_lib.is_similar_strings("AC/DC", "ac dc")
    assert not similarity_lib.is_similar_strings("AC/DC", "kiejfriufruh")
