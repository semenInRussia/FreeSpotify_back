import pytest

from FreeSpotify_back.music_manager.core.exceptions import NotFoundAlbumError
from FreeSpotify_back.music_manager.implementations import Rocknation

artist_name = "queen"
album_name = "Jazz"

album_params = {"artist_name": artist_name, "album_name": album_name}

not_valid_params = {
    "artist_name": "AC/DC",
    "album_name": "oafihfaiertghuhrguhtguhtughtuhgusefjvnmvcmxpweqopqp[wqpewqpirrofqrfiju`",
}


@pytest.fixture()
def rocknation():
    return Rocknation()


def test_get_link(rocknation: Rocknation):
    assert (
        rocknation.albums.get_link(**album_params)
        == "http://rocknation.su/mp3/album-792"
    )


def test_get_link_should_raise_not_found_album(rocknation: Rocknation):
    with pytest.raises(NotFoundAlbumError):
        rocknation.albums.get_link(artist_name, "adhhrfeushfuehreururhgurheguirhegueg")


def test_get_link_on_album_on_page_with_nest(rocknation: Rocknation):
    actual = rocknation.albums.get_link("AC/DC", "Power UP")

    assert actual == "http://rocknation.su/mp3/album-5861"


def test_get_link_on_img(rocknation: Rocknation):
    assert (
        rocknation.albums.get_link_on_img(**album_params)
        == "http://rocknation.su/upload/images/albums/792.jpg"
    )
