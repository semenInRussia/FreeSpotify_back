import pytest

from dto import ArtistDto
from entities import Artist
from entities.track import Track

artist_name = "Metallica"
approximate_artist_name = "metallica"


@pytest.fixture
def artist():
    return Artist(artist_name=approximate_artist_name)


def test_get_precise_artist_name(artist):
    assert artist.name == artist_name


def _assert_is_track_top(top):
    assert len(top) == 10

    assert isinstance(top[0], Track)


def test_get_top(artist):
    top = artist.top

    _assert_is_track_top(top)


def test_create_from_dto():
    dto = ArtistDto(artist_name)

    artist = Artist.create_from_dto(dto)

    assert isinstance(artist, Artist)


def test_get_link(artist):
    assert artist.link == "https://rocknation.su/mp3/band-31"


def test_get_link_on_img(artist):
    assert artist.link_on_img == "https://rocknation.su/upload/images/bands/31.jpg"


def test_get_all_data_beside_top(artist):
    data = artist.data.get_serialized_data('name', 'link', 'link_on_img')

    assert 'name' in data
    assert 'link' in data
    assert 'link_on_img' in data