import pytest

from dto import ArtistDto
from entities import Artist
from entities.track import Track
from tests.settigs_for_test import settings_with_mock

artist_name = "Metallica"
approximate_artist_name = "metallica"


@pytest.fixture
def artist():
    return Artist(artist_name=approximate_artist_name, additional_settings=settings_with_mock)

def test_work_with_settings(artist):
    assert artist.settings.music_manager_impl == settings_with_mock.music_manager_impl

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


