from collections.abc import Iterable
from pathlib import Path

from FreeSpotify_back.my_os import (
    dirs,
    dirs_similar_to,
    file_without_file_extension,
    join_all_paths_with,
    parse_path,
    search_dirs_by_pattern,
)

THIS_FILE = Path(__file__)
PATH_TO_DIR = str((THIS_FILE.parent / "test_os").resolve())


def _is_equal_paths(path1: str, path2: str) -> bool:
    return parse_path(path1) == parse_path(path2)


def _is_equal_paths_collection(
    path_collection1: Iterable[str], path_collection2: Iterable[str],
) -> bool:
    parsed_path_collection1 = list(map(parse_path, path_collection1))
    parsed_path_collection2 = list(map(parse_path, path_collection2))

    return parsed_path_collection1 == parsed_path_collection2


def test_parse_path():
    assert (
        parse_path("music/artist/album") == "music\\artist\\album"
        or parse_path("music/artist/album") == "music/artist/album"
    )


def test_dirs():
    assert _is_equal_paths_collection(
        dirs(PATH_TO_DIR),
        [
            f"{PATH_TO_DIR}/folder",
            f"{PATH_TO_DIR}/subdir1",
            f"{PATH_TO_DIR}/subdir2",
        ],
    )


def test_dirs_similar_to():
    assert _is_equal_paths_collection(
        dirs_similar_to("subdir 2", PATH_TO_DIR),
        [f"{PATH_TO_DIR}/subdir2", f"{PATH_TO_DIR}/subdir1"],
    )
    assert _is_equal_paths_collection(
        dirs_similar_to("subdir", f"{PATH_TO_DIR}/subdir1"),
        [f"{PATH_TO_DIR}/subdir1/dir1", f"{PATH_TO_DIR}/subdir1/dir2"],
    )


def test_search_dirs():
    actual = search_dirs_by_pattern(f"{PATH_TO_DIR}/~subdir")
    assert _is_equal_paths_collection(
        actual, [f"{PATH_TO_DIR}/subdir1", f"{PATH_TO_DIR}/subdir2"],
    )


def test_search_dirs_with_double_nesting():
    actual = search_dirs_by_pattern(f"{PATH_TO_DIR}/~subdir/~dir")
    assert _is_equal_paths_collection(
        list(actual),
        [
            f"{PATH_TO_DIR}/subdir1/dir1",
            f"{PATH_TO_DIR}/subdir1/dir2",
            f"{PATH_TO_DIR}/subdir2/dir3",
            f"{PATH_TO_DIR}/subdir2/dir4",
        ],
    )


def test_search_dirs_using_star():
    search_dirs_by_pattern(f"{PATH_TO_DIR}/*")


def test_join_all_paths_with():
    actual = join_all_paths_with("dir", ["dir1", "dir2"])
    assert _is_equal_paths_collection(list(actual), ["dir1/dir", "dir2/dir"])


def test_file_without_file_extension():
    assert file_without_file_extension("test_my_os.py") == "test_my_os"
