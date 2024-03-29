from FreeSpotify_back.music_manager.utils import delete_sound_quality
from FreeSpotify_back.music_manager.utils import delete_year_in_album_name


def test_delete_year_in_album_name():
    assert (
        delete_year_in_album_name("1883 - Bach - St. Matthew Passion")
        == "Bach - St. Matthew Passion"
    )


def test_delete_sound_quality():
    actual = delete_sound_quality("Black Sabbath (Remastered 2008)")

    assert actual == "Black Sabbath"

    actual = delete_sound_quality("Black Sabbath [Premium Disk]")

    assert actual == "Black Sabbath"

    actual = delete_sound_quality("Burn - remastered 2012")

    assert actual == "Burn"

    actual = delete_sound_quality("In Utero - 20th Anniversary - Deluxe Edition")

    assert actual == "In Utero"
