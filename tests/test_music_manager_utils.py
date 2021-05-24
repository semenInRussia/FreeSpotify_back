from music_manger.utils import delete_sound_quality
from music_manger.utils import delete_year_in_album_name


def test_delete_year_in_album_name():
    assert delete_year_in_album_name("1883 - Bach - St. Matthew Passion") == "Bach - St. Matthew Passion"


def test_delete_sound_quality():
    expected = delete_sound_quality("Black Sabbath (Remastered 2008)")

    assert "Black Sabbath" == expected

    expected = delete_sound_quality("Black Sabbath [Premium Disk]")

    assert "Black Sabbath" == expected
