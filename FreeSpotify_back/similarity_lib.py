import difflib
from collections.abc import Callable, Iterable
from typing import Optional, TypeVar

DEFAULT_MIN_RATIO_OF_SIMILARITY = 0.6

Element = TypeVar("Element")
_Key = Optional[Callable[[Element], str]]

T = TypeVar("T")


def search_string_similar_to(
    string: str, strings: Iterable[T], key: _Key[T] = None
) -> T:
    """Return the most similar to the given string.

    You can pass a list of objects (not strings) and function that return string,
    the resulting strings will be compared with the given
    """
    return next(iter(sort_objects_by_similarity_to(string, strings, key=key)))


T = TypeVar("T")


def filter_and_sort_strings_by_min_similarity_to(
    string: str,
    strings: Iterable[T],
    min_ratio_of_similarity: float = DEFAULT_MIN_RATIO_OF_SIMILARITY,
    key: _Key[T] = None,
) -> Iterable[T]:
    """Return the most similar to the given strings.

    You can pass a list of objects (not strings) and function that return string,
    the resulting strings will be compared with the given

    Similarity measured as number from 0 to 1, you can provide the number what
    you need to remove
    """
    filtered_strings = filter_objects_by_min_similarity_to(
        string, strings, min_ratio_of_similarity, key=key
    )
    return sort_objects_by_similarity_to(string, filtered_strings, key=key)


T = TypeVar("T")


def filter_objects_by_min_similarity_to(
    string: str,
    objects: Iterable[T],
    min_ratio_of_similarity: Optional[float] = None,
    key: _Key[T] = None,
) -> Iterable[T]:
    """Remove from the given strings strings that aren't similar to the given.

    You can pass a list of objects (not strings) and function that return string,
    the resulting strings will be compared with the given

    Similarity measured as number from 0 to 1, you can provide the number what
    you need to remove
    """
    _key = key or str
    return filter(
        lambda o: is_similar_strings(_key(o), string, min_ratio_of_similarity), objects
    )


def is_similar_strings(
    actual: str, expected: str, min_ratio: Optional[float] = None
) -> bool:
    """Return True, if given strings are similar.

    Similarity measured as number from 0 to 1, you can provide that indicates that
    strings are similar
    """
    if min_ratio is None:
        min_ratio = DEFAULT_MIN_RATIO_OF_SIMILARITY

    ratio = get_ratio_of_similarity(actual, expected)

    return ratio > min_ratio


def get_ratio_of_similarity(actual: str, expected: str) -> float:
    """Return number from 0 to 1 that tell about similarity between given strings."""
    normalized_actual, normalized_excepted = (
        _normalize_string(actual),
        _normalize_string(expected),
    )

    matcher = difflib.SequenceMatcher(None, normalized_actual, normalized_excepted)

    return matcher.ratio()


def _normalize_string(string: str) -> str:
    return string.lower()


T = TypeVar("T")


def sort_objects_by_similarity_to(
    string: str, objects: Iterable[T], key: _Key[T] = None
) -> Iterable[T]:
    """Sort given strings with the similarity to the given.

    You can pass a list of objects (not strings) and function that return string,
    the resulting strings will be compared with the given
    """
    if key is None:
        key = str
    return iter(sorted(objects, key=lambda o: -get_ratio_of_similarity(key(o), string)))
