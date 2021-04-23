import os
from typing import List

from similarity_lib import filter_and_sort_strings_by_min_similarity_to


def dirs_similar_to(string_for_compare: str, path: str) -> List[str]:
    return filter_and_sort_strings_by_min_similarity_to(
        string_for_compare,
        dirs(path)
    )


def dirs(path: str) -> List[str]:
    return os.listdir(parse_path(path))


def parse_path(path: str) -> str:
    res = ""

    for path_part in path.split("/"):
        res = os.path.join(res, path_part)

    return res
