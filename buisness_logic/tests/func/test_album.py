import pytest

from buisness_logic.dto import AlbumDto
from buisness_logic.entities.album import Album

album_name = "Paranoid"
artist_name = "Black sabbath"

release_date = "1970-09-18"

approximate_album_name = "paranoid  "

@pytest.fixture
def album():
    return Album(artist_name, album_name)

def test_precise_name(album):
    assert album.name == album_name

def test_release_year(album):
    assert album.release_date == release_date

def test_create_from_dto():
    dto = AlbumDto(artist_name, album_name)

    album = Album.create_from_dto(dto)

    assert isinstance(album, Album)
