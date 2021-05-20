import pytest

from music_manger.core.exceptions import NotFoundTrackException
from music_manger.implementations.rocknation_and_spotify.rocknation.rocknationAPI import Rocknation

artist_name = "nirvana"
album_name = "In Ultero"
track_name = "tourette"


@pytest.fixture()
def rocknation():
    return Rocknation()


def test_get_link(rocknation):
    actual = rocknation.tracks.get_link(artist_name, album_name, track_name)

    assert actual == "http://rocknation.su/upload/mp3/Nirvana/1993%20-%20In%20Utero/11.%20Tourette%27s.mp3"


def test_get_link_on_single(rocknation):
    actual = rocknation.tracks.get_link(
        "Kiss",
        "Hotter than hell",
        "Hotter than hell"
    )

    excepted = "http://rocknation.su/upload/mp3/Kiss/1974%20-%20Hotter%20Than%20Hell/04.%20Hotter%20Than%20Hell.mp3"

    assert actual == excepted


def test_get_link_should_raise_exception(rocknation):
    with pytest.raises(NotFoundTrackException):
        link = rocknation.tracks.get_link(
            artist_name,
            album_name,
            "jiferihguthughtughtughtughtughtugkdfrkrjfirmc,nvtjugtugn"
        )


def test_get_link_on_image(rocknation):
    excepted = "http://rocknation.su/upload/images/albums/781.jpg"

    assert rocknation.tracks.get_link_on_img(artist_name, album_name, track_name) == excepted
