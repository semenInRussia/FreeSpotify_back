import pytest

from FreeSpotify_back.dto import ArtistDto
from FreeSpotify_back.entities import Album
from FreeSpotify_back.entities import Artist
from FreeSpotify_back.entities.track import Track
from ..settigs_for_test import settings_with_mock

artist_name = "Metallica"
approximate_artist_name = "metallica"
difference_name = "Megadeth"

additional_settings = settings_with_mock


@pytest.fixture
def artist():
    return Artist(artist_name=approximate_artist_name,
                  additional_settings=settings_with_mock)


@pytest.fixture()
def artist_dto():
    return ArtistDto(name=artist_name)


def test_get_name(artist: Artist):
    assert isinstance(artist.name, str)


def test_work_with_settings(artist):
    assert artist.settings.music_manager_impl == settings_with_mock.music_manager_impl


def test_equal_artists():
    first_artist = Artist(artist_name, additional_settings=additional_settings)
    second_artist = Artist(artist_name, additional_settings=additional_settings)

    assert first_artist == second_artist


def test_notequal_artists():
    first_artist = Artist(artist_name, additional_settings=additional_settings)
    second_artist = Artist(difference_name, additional_settings=additional_settings)

    assert first_artist != second_artist


def test_notequal_artist_with_other_types():
    assert Artist(artist_name, additional_settings=additional_settings) != 0
    assert Artist(artist_name, additional_settings=additional_settings) != "STRING"


def _assert_is_track_top(top):
    assert len(top) == 10

    assert isinstance(top[0], Track)


def test_get_top(artist):
    top = artist.top

    _assert_is_track_top(top)

def test_get_top_by_not_valid_track_names():
    artist = Artist(artist_name)

    top = artist.top

    # Get all tracks' links
    list(map(
        lambda track: track.link,
        top
    ))

    assert isinstance(top, list)


def test_get_albums(artist: Artist):
    albums = artist.albums

    assert albums
    assert isinstance(albums, list)

    assert isinstance(albums[0], Album)


def test_create_from_dto(artist_dto: ArtistDto):
    artist = Artist.create_from_dto(artist_dto, additional_settings=additional_settings)

    assert isinstance(artist, Artist)


def test_work_with_settings_when_create_from_dto(artist_dto: ArtistDto):
    artist = Artist.create_from_dto(artist_dto, additional_settings=settings_with_mock)

    assert settings_with_mock.music_manager_impl == artist.settings.music_manager_impl


def test_get_link(artist):
    assert isinstance(artist.link, str)


def test_get_link_on_img(artist):
    assert isinstance(artist.link_on_img, str)
