import similarity_lib

test_strings = ["a", "ac dc", "b", "AC/DC", "AC/dc"]


def test_filter_and_sort_strings_by_min_similarity_to():
    expected = similarity_lib.filter_and_sort_strings_by_min_similarity_to("AC/DC",
                                                                           ["a", "ac dc", "b", "AC/DC", "AC/dc"])

    assert ["AC/DC", "AC/dc", "ac dc"] == expected


def test_filter_strings_by_min_similarity_to():
    expected = similarity_lib.filter_strings_by_min_similarity_to("AC/DC",
                                                                  ["b", "jrfihguthrgtgitjht", "kdkoooo", "ac dc"])

    assert ["ac dc"] == expected


def test_is_similar_strings():
    assert similarity_lib.is_similar_strings("AC/DC", "ac dc")
    assert not similarity_lib.is_similar_strings("AC/DC", "kiejfriufruh")


def test_sort_strings_by_similarity_to():
    excepted = similarity_lib.sort_strings_by_similarity_to("AC/DC", ["AC DC", "AC/DC", "ac dc", "a", "acdc"])

    assert ['AC/DC', 'acdc', 'AC DC', 'ac dc', 'a'] == excepted
