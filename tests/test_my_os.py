from my_os import parse_path, dirs, dirs_similar_to


def test_parse_path():
    assert parse_path("music/artist/album") == "music\\artist\\album" or \
           parse_path("music/artist/album") == "music/artist/album"


def test_dirs():
    assert dirs("dir") == ["subdir1", "subdir2"]


def test_dirs_similar_to():
    assert dirs_similar_to("subdir 2", "dir") == ["subdir2", "subdir1"]
