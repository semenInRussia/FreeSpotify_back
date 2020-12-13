import pytest

from buisness_logic.dto import ArtistDto
from buisness_logic.entities.artist import Artist
from buisness_logic.entities.track import Track

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
