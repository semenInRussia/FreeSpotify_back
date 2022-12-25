import difflib

from typing import Callable
from typing import Iterable
from typing import Optional
from typing import TypeVar

DEFAULT_MIN_RATIO_OF_SIMILARITY = 0.6
O = TypeVar("O")
_Key = Optional[Callable[[O], str]]

def search_string_similar_to(string: str,
                             strings: Iterable[O],
                             key: _Key=None) -> O:
    return next(iter(sort_objects_by_similarity_to(string, strings, key=key)))


def filter_and_sort_strings_by_min_similarity_to(string: str,
                                                 strings: Iterable[O],
                                                 min_ratio_of_similarity=DEFAULT_MIN_RATIO_OF_SIMILARITY,
                                                 key: _Key=None
                                                 ) -> Iterable[O]:
    filtered_strings = filter_objects_by_min_similarity_to(string,
        strings, min_ratio_of_similarity, key=key)
    sorted_objects = sort_objects_by_similarity_to(string,
        filtered_strings,
        key=key)

    return sorted_objects


def filter_objects_by_min_similarity_to(
        string: str,
        objects: Iterable[O],
        min_ratio_of_similarity: Optional[float]=None,
        key: _Key=None) -> Iterable[O]:
    _key: Callable[[O], str] = key or str
    return filter(
        lambda o: is_similar_strings(_key(o), string, min_ratio_of_similarity),
        objects)


def is_similar_strings(actual: str,
                       expected: str,
                       min_ratio: Optional[float]=None) -> bool:
    if min_ratio is None:
        min_ratio = DEFAULT_MIN_RATIO_OF_SIMILARITY

    ratio = get_ratio_of_similarity(actual, expected)

    return ratio > min_ratio


def get_ratio_of_similarity(actual: str, expected: str) -> float:
    normalized_actual, normalized_excepted = (
        _normalize_string(actual),
        _normalize_string(expected))

    matcher = difflib.SequenceMatcher(
        None,
        normalized_actual,
        normalized_excepted)

    return matcher.ratio()


def _normalize_string(string: str) -> str:
    return string.lower()


def sort_objects_by_similarity_to(string: str,
                                  objects: Iterable[O],
                                  key: _Key=None) -> Iterable[O]:
    if key is None:
        key = str
    return iter(sorted(objects,
                       key=lambda o: -get_ratio_of_similarity(key(o), string)))
