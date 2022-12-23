import difflib
from typing import Callable
from typing import List
from typing import Optional
from typing import Iterable
from typing import TypeVar

DEFAULT_MIN_RATIO_OF_SIMILARITY = 0.6


def search_string_similar_to(string: str, strings: List[str], key=None) -> str:
    return sort_objects_by_similarity_to(string, strings, key=key)[0]


def filter_and_sort_strings_by_min_similarity_to(
        string: str,
        strings: List[str],
        min_ratio_of_similarity=DEFAULT_MIN_RATIO_OF_SIMILARITY
) -> List[str]:
    filtered_strings = filter_strings_by_min_similarity_to(
        string,
        strings,
        min_ratio_of_similarity
    )
    sorted_strings = sort_objects_by_similarity_to(string, filtered_strings)

    return sorted_strings


def filter_strings_by_min_similarity_to(
        string: str,
        strings: List[str],
        min_ratio_of_similarity: Optional[float]=None) -> List[str]:
    return list(filter(
        lambda actual_string: is_similar_strings(
            actual_string,
            string,
            min_ratio_of_similarity
        ),
        strings
    ))


def is_similar_strings(actual: str,
                       expected: str, min_ratio: Optional[float]=None) -> bool:
    """Is similar actual string to excepted string?"""
    if min_ratio is None:
        min_ratio = DEFAULT_MIN_RATIO_OF_SIMILARITY

    ratio = get_ratio_of_similarity(actual, expected)

    return ratio > min_ratio


def get_ratio_of_similarity(actual: str, expected: str) -> float:
    """
    Diff two strings, return ratio of similarity Float Number min 0 max 1.
    """
    normalized_actual, normalized_excepted = (
        _normalize_string(actual),
        _normalize_string(expected)
    )

    matcher = difflib.SequenceMatcher(
        None,
        normalized_actual,
        normalized_excepted
    )

    return matcher.ratio()


def _normalize_string(string: str) -> str:
    return string.lower()


O = TypeVar("O")

def sort_objects_by_similarity_to(string: str,
                                  objects: Iterable[O],
                                  key: Callable[[O], str]=str
                                  ) -> List[str]:
    strings = map(key, objects)
    return sorted(strings,
                  key=lambda s: -get_ratio_of_similarity(s, string))
