from functools import reduce
import os
import pathlib
from typing import List

from _low_level_utils import sum_of_lists
from similarity_lib import filter_and_sort_strings_by_min_similarity_to

SIMILARITY_TARGET = '~'
SIMILARITY_TARGET_LENGTH = 1

DEFAULT_MIN_RATIO_OF_SIMILARITY_FILENAMES = 0.5


def dirs_similar_to(string_for_compare: str, path: str) -> List[str]:
    return list(map(
        lambda dir_name: os.path.join(path, dir_name),

        dirs_names_similar_to(string_for_compare, path)
    ))


def dirs_names_similar_to(string_for_compare: str, path: str) -> List[str]:
    return filter_and_sort_strings_by_min_similarity_to(
        string_for_compare,
        dirs_names(path),

        DEFAULT_MIN_RATIO_OF_SIMILARITY_FILENAMES
    )


def dirs_names(path: str) -> List[str]:
    try:
        return os.listdir(parse_path(path))
    except NotADirectoryError:
        return []


def dirs(path: str) -> List[str]:
    return list(map(
        lambda dir_name: os.path.join(path, dir_name),

        dirs_names(path)
    ))


def parse_path(path: str) -> str:
    if path == '':
        return '.'

    return reduce(
        os.path.join,
        path.split('/')
    )


def get_parts_of_path(path: str):
    return pathlib.Path(path).parts


def search_dirs_by_pattern(pattern: str) -> List[str]:
    found_dirs = [""]

    pattern = parse_path(pattern)
    parts_of_patterns = get_parts_of_path(pattern)

    possible_search_expressions = [
        SimilarSearchExpression(),
        AllDirsSearchExpression(),
        DefaultSearchExpression()
    ]

    for expression in parts_of_patterns:
        for search_expression in possible_search_expressions:
            if search_expression.is_this_expression(expression):
                found_dirs = search_expression.get_listdir_from_dirs(found_dirs, expression)
                break

    return found_dirs


class SearchExpression:
    def is_this_expression(self, string: str) -> bool:
        pass

    def get_listdir_from_dirs(self, paths: List[str], concrete_expression: str) -> List[str]:
        pass


class SimilarSearchExpression(SearchExpression):
    token: str = '~'
    token_length: int = 1

    def get_listdir_from_dirs(self, paths: List[str], concrete_expression: str) -> List[str]:
        string_for_compare = self._ignore_token(concrete_expression)

        listdir = list(map(
            lambda path: dirs_similar_to(string_for_compare, path),
            paths
        ))

        listdir = sum_of_lists(*listdir)

        return listdir

    def _ignore_token(self, string: str) -> str:
        return string[self.token_length:]

    def is_this_expression(self, string: str) -> bool:
        return string.startswith(self.token)


class AllDirsSearchExpression(SearchExpression):
    token = '*'

    def get_listdir_from_dirs(self, paths: List[str], concrete_expression: str) -> List[str]:
        listdir = list(map(
            lambda path: dirs(path),
            paths
        ))

        listdir = sum_of_lists(*listdir)

        return listdir

    def is_this_expression(self, string: str) -> bool:
        return string.startswith(self.token)


class DefaultSearchExpression(SearchExpression):
    def get_listdir_from_dirs(self, paths: List[str], concrete_expression: str) -> List[str]:
        return join_all_paths_with(concrete_expression, paths)

    def is_this_expression(self, string: str) -> bool:
        return True


def join_all_paths_with(path_for_joining: str, paths: List[str]):
    return list(map(
        lambda path: os.path.join(path, path_for_joining),

        paths
    ))


def file_without_file_extension(path: str) -> str:
    parts_of_filename = path.split('.')

    return ''.join(parts_of_filename[:-1])
