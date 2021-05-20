import pytest

from music_manger.core.exceptions import NotFoundArtistException
from music_manger.implementations.rocknation_and_spotify.rocknation.rocknationAPI import Rocknation

artist_name = "AC DC"

not_valid_params = {
    "artist_name": "#udheuwgfyregfyrgfygrfygryfgryfgy-"
}

artist_params = {
    "artist_name": artist_name
}


@pytest.fixture()
def rocknation():
    return Rocknation()


def test_get_link(rocknation: Rocknation):
    assert rocknation.artists.get_link(**artist_params) == "http://rocknation.su/mp3/band-1"


def test_get_link_should_raise_not_found_exception(rocknation: Rocknation):
    with pytest.raises(NotFoundArtistException):
        artist = rocknation.artists.get_link(**not_valid_params)


def test_get_link_on_img(rocknation: Rocknation):
    assert rocknation.artists.get_link_on_img(**artist_params) == "http://rocknation.su/upload/images/bands/1.jpg"
