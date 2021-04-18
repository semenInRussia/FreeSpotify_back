from music_manger.implementations.rocknation_and_spotify.utils import delete_sound_quality


def test_delete_sound_quality():
    expected = delete_sound_quality("Black Sabbath (Remastered 2008)")

    assert "Black Sabbath" == expected

    expected = delete_sound_quality("Black Sabbath [Premium Disk]")

    assert "Black Sabbath" == expected
