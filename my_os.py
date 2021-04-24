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
    return os.listdir(parse_path(path))


def dirs(path: str) -> List[str]:
    return list(map(
        lambda dir_name: os.path.join(path, dir_name),

        dirs_names(path)
    ))


def parse_path(path: str) -> str:
    res = ""

    for path_part in path.split("/"):
        res = os.path.join(res, path_part)

    return res


def search_dirs_by_pattern(pattern: str) -> List[str]:
    pattern = parse_path(pattern)

    found_dirs = [""]
    parts_of_patterns = pathlib.Path(pattern).parts

    for part_of_pattern in parts_of_patterns:
        if _is_pattern_similarity(part_of_pattern):
            just_found_dirs = list(map(
                lambda found_dir: dirs_similar_to(_ignore_target_similarity(part_of_pattern), found_dir),
                found_dirs
            ))

            just_found_dirs = sum_of_lists(*just_found_dirs)

            found_dirs = just_found_dirs
        else:
            found_dirs = join_all_paths_with(part_of_pattern, found_dirs)

    return found_dirs


def _is_pattern_similarity(pattern: str) -> bool:
    return pattern[0] == SIMILARITY_TARGET


def _ignore_target_similarity(pattern: str) -> str:
    return pattern[SIMILARITY_TARGET_LENGTH:]


def join_all_paths_with(path_for_joining: str, paths: List[str]):
    return list(map(
        lambda path: os.path.join(path, path_for_joining),

        paths
    ))
