import pytest

from music_manger.core.exceptions import NotFoundAlbumException
from music_manger.core.exceptions import NotFoundArtistException
from music_manger.implementations.rocknation_and_spotify.rocknation.rocknationAPI import Rocknation

artist_name = "queen"
album_name = "Jazz"

album_params = {
    "artist_name": artist_name,
    "album_name": album_name
}

not_valid_params = {
    "artist_name": "jdsjifhrgurhegeia",
    "album_name": "oafihfaiertghuhrguhtguhtughtuhgusefjvnmvcmxpweqopqp[wqpewqpirrofqrfiju`"
}


@pytest.fixture()
def rocknation():
    return Rocknation()


def test_get_link(rocknation: Rocknation):
    assert rocknation.albums.get_link(**album_params) == "http://rocknation.su/mp3/album-792"


def test_get_link_should_raise_not_found(rocknation: Rocknation):
    with pytest.raises(NotFoundArtistException):
        album = rocknation.albums.get_link(**not_valid_params)
        assert album is None


def test_get_link_should_raise_not_found_album(rocknation: Rocknation):
    with pytest.raises(NotFoundAlbumException):
        album = rocknation.albums.get_link(artist_name, "adhhrfeushfuehreururhgurheguirhegueg")
        assert album is None


def test_get_link_on_img(rocknation: Rocknation):
    assert rocknation.albums.get_link_on_img(**album_params) == "http://rocknation.su/upload/images/albums/792.jpg"
