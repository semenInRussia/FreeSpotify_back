import os
import pathlib
from collections.abc import Iterable
from itertools import chain
from pathlib import Path

from .similarity_lib import filter_and_sort_strings_by_min_similarity_to

SIMILARITY_TARGET = "~"
SIMILARITY_TARGET_LENGTH = 1

DEFAULT_MIN_RATIO_OF_SIMILARITY_FILENAMES = 0.5


def dirs_similar_to(string_for_compare: str, path: str) -> Iterable[str]:
    """Return directories pathes that similar to the given string in the given path."""
    for dir_name in dirs_names_similar_to(string_for_compare, path):
        yield str(Path(path) / dir_name)


def dirs_names_similar_to(string_for_compare: str, path: str) -> Iterable[str]:
    """Return directories names that similar to the given string in the given path."""
    return filter_and_sort_strings_by_min_similarity_to(
        string_for_compare, dirs_names(path), DEFAULT_MIN_RATIO_OF_SIMILARITY_FILENAMES
    )


def dirs_names(path: str) -> Iterable[str]:
    """Return names of the subdirectories that a given directory consist of."""
    try:
        return os.listdir(parse_path(path))
    except NotADirectoryError:
        return []


def dirs(path: str) -> Iterable[str]:
    """Return pathes of the subdirectories that a given directory consist of."""
    for dir_name in dirs_names(path):
        yield str(Path(path) / dir_name)


def parse_path(path: str) -> str:
    """Make a given path more standard."""
    if not path:
        return "."
    return os.path.join(*path.split("/"))


def get_parts_of_path(path: str) -> Iterable[str]:
    """Return list from the parts of a given path."""
    return pathlib.Path(path).parts


def search_dirs_by_pattern(pattern: str) -> Iterable[str]:
    """Return list of directories that matches with a given pattern.

    Pattern is a normal file/directory path in where a part can be *, that means return
    every subdir, a just name or a name with ~ at the start that means return every
    subdir name that similar to the next word (after tilda)
    """
    found_dirs = [""]

    pattern = parse_path(pattern)
    parts_of_patterns = get_parts_of_path(pattern)

    possible_search_expressions = [
        _SimilarSearchExpression(),
        _AllDirsSearchExpression(),
        _DefaultSearchExpression(),
    ]

    for expression in parts_of_patterns:
        for search_expression in possible_search_expressions:
            if search_expression.is_this_expression(expression):
                found_dirs = search_expression.get_listdir_from_dirs(
                    found_dirs, expression
                )
                break

    return found_dirs


class _SearchExpression:
    def is_this_expression(self, _string: str) -> bool:
        return NotImplemented

    def get_listdir_from_dirs(
        self, _paths: Iterable[str], _concrete_expression: str
    ) -> Iterable[str]:
        return NotImplemented


class _SimilarSearchExpression(_SearchExpression):
    token: str = "~"
    token_length: int = 1

    def get_listdir_from_dirs(
        self, paths: Iterable[str], concrete_expression: str
    ) -> Iterable[str]:
        string_for_compare = self._ignore_token(concrete_expression)

        return chain.from_iterable(
            [dirs_similar_to(string_for_compare, path) for path in paths]
        )

    def _ignore_token(self, string: str) -> str:
        return string[self.token_length :]

    def is_this_expression(self, string: str) -> bool:
        return string.startswith(self.token)


class _AllDirsSearchExpression(_SearchExpression):
    token = "*"

    def get_listdir_from_dirs(
        self, paths: Iterable[str], _concrete_expression: str
    ) -> Iterable[str]:
        return chain.from_iterable(map(dirs, paths))

    def is_this_expression(self, string: str) -> bool:
        return string.startswith(self.token)


class _DefaultSearchExpression(_SearchExpression):
    def get_listdir_from_dirs(
        self, paths: Iterable[str], concrete_expression: str
    ) -> Iterable[str]:
        return join_all_paths_with(concrete_expression, paths)

    def is_this_expression(self, _string: str) -> bool:
        return True


def join_all_paths_with(path_for_joining: str, paths: Iterable[str]) -> Iterable[str]:
    """Join every name with the given path base."""
    for path in paths:
        yield str(Path(path) / path_for_joining)


def file_without_file_extension(path: str) -> str:
    """Chop from a path extension."""
    parts_of_filename = path.split(".")
    return "".join(parts_of_filename[:-1])
