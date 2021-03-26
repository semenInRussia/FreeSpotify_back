
import difflib
from typing import List

DEFAULT_MIN_RATIO_OF_SIMILARITY = 0.6

def filter_and_sort_strings_by_min_similarity_to(
        string: str,
        strings: List[str],
        min_ratio_of_similarity=DEFAULT_MIN_RATIO_OF_SIMILARITY) -> List[str]:
    """
    Get all similar strings from list of strings.

    For example:
`   >>> _get_actual_strings_similar_to_excepted(["System", "System of a down", "AC/DC"], "system")
    ['System', 'System of a down']
    """

    filtered_strings = filter_strings_by_min_similarity_to(string, strings, min_ratio_of_similarity)
    sorted_strings = sort_strings_by_similarity_to(string, filtered_strings)

    return sorted_strings


def filter_strings_by_min_similarity_to(string: str,
                                        strings: List[str],
                                        min_ratio_of_similarity: float = None) -> List[str]:
    return list(filter(
        lambda actual_string: is_similar_strings(actual_string, string, min_ratio_of_similarity),

        strings
    ))


def is_similar_strings(actual: str, expected: str, min_ratio: float = None) -> bool:
    """Is similar actual string to excepted string?"""
    if min_ratio is None:
        min_ratio = DEFAULT_MIN_RATIO_OF_SIMILARITY

    ratio = get_ratio_of_similarity(actual, expected)

    return ratio > min_ratio


def get_ratio_of_similarity(actual: str, expected: str) -> float:
    """
    Diff two strings, return ratio of similarity Float Number min 0 max 1.
    """
    normalized_actual, normalized_excepted = _normalize_string(actual), _normalize_string(expected)

    matcher = difflib.SequenceMatcher(None, normalized_actual, normalized_excepted)

    return matcher.ratio()


def _normalize_string(string: str) -> str:
    return string.lower()


def sort_strings_by_similarity_to(string: str, strings: List[str]) -> List[str]:
    return sorted(
        strings,
        key=lambda excepted_string: -(get_ratio_of_similarity(string, excepted_string))
    )
