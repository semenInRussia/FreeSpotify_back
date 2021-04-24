from my_os import dirs, join_all_paths_with
from my_os import dirs_similar_to
from my_os import parse_path
from my_os import search_dirs_by_pattern


def _is_equal_paths(path1: str, path2: str):
    return parse_path(path1) == parse_path(path2)


def _is_equal_paths_collection(path_collection1, path_collection2):
    parsed_path_collection1 = list(map(parse_path, path_collection1))
    parsed_path_collection2 = list(map(parse_path, path_collection2))

    return parsed_path_collection1 == parsed_path_collection2


def test_parse_path():
    assert parse_path("music/artist/album") == "music\\artist\\album" or \
           parse_path("music/artist/album") == "music/artist/album"


def test_dirs():
    assert _is_equal_paths_collection(dirs("dir"), ["dir/folder", "dir/subdir1", "dir/subdir2"])


def test_dirs_similar_to():
    assert _is_equal_paths_collection(
        dirs_similar_to("subdir 2", "dir"),
        ["dir/subdir2", "dir/subdir1"]
    )

    assert _is_equal_paths_collection(
        dirs_similar_to("subdir", "dir/subdir1"),
        ["dir/subdir1/dir1", "dir/subdir1/dir2"]
    )


def test_search_dirs():
    actual = search_dirs_by_pattern("dir/~subdir")

    assert _is_equal_paths_collection(actual, ["dir/subdir1", "dir/subdir2"])


def test_search_dirs_with_double_nesting():
    actual = search_dirs_by_pattern("dir/~subdir/~dir")

    assert _is_equal_paths_collection(actual,
                                      ["dir/subdir1/dir1", "dir/subdir1/dir2", "dir/subdir2/dir3", "dir/subdir2/dir4"])


def test_join_all_paths_with():
    actual = join_all_paths_with("dir", ["dir1", "dir2"])

    assert _is_equal_paths_collection(actual, ["dir1/dir", "dir2/dir"])
