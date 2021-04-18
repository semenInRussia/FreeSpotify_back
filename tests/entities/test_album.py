import pytest

from dto import AlbumDto
from entities import Album, Artist
from entities.track import Track
from tests.settigs_for_test import settings_with_mock

album_name = "Paranoid"
artist_name = "Black sabbath"

difference_artist_name = "DIO"
difference_album_name = "Sabbath Bloody Sabbath"

release_date = "1970-09-18"
approximate_album_name = "paranoid  "
num_tracks_in_album = 8

additional_settings = settings_with_mock


@pytest.fixture
def album():
    return Album(artist_name, album_name, additional_settings=additional_settings)


def test_get_name(album):
    assert isinstance(album.name, str)


def test_work_with_settings(album):
    assert album.settings.music_manager_impl == settings_with_mock.music_manager_impl


def test_get_release_date(album):
    assert isinstance(album.release_date, str)


def test_create_from_dto():
    dto = AlbumDto(artist_name, album_name)

    album = Album.create_from_dto(dto, additional_settings=additional_settings)

    assert isinstance(album, Album)


def test_get_tracks(album):
    tracks = album.tracks

    assert isinstance(tracks[0], Track)
    assert len(tracks)


def test_get_link(album):
    assert isinstance(album.link, str)


def test_get_link_on_img(album):
    assert isinstance(album.link_on_img, str)


def test_work_with_settings_when_create_from_dto():
    album_dto = AlbumDto(artist_name, album_name)
    album = Album.create_from_dto(album_dto, additional_settings=settings_with_mock)

    assert album.settings.music_manager_impl == settings_with_mock.music_manager_impl


def test_equal_albums():
    first_album = Album(artist_name, album_name, additional_settings=additional_settings)
    second_album = Album(artist_name, album_name, additional_settings=additional_settings)

    assert first_album == second_album


def test_notequal_by_artist_albums():
    first_album = Album(artist_name, album_name, additional_settings=additional_settings)
    second_album = Album(difference_artist_name, album_name, additional_settings=additional_settings)

    assert first_album != second_album


def test_notequal_by_name_albums():
    first_album = Album(artist_name, album_name, additional_settings=additional_settings)
    second_album = Album(artist_name, difference_album_name, additional_settings=additional_settings)

    assert first_album != second_album


def test_notequal_with_other_type():
    assert Album(artist_name, album_name, additional_settings=additional_settings) != 1
    assert Album(artist_name, album_name, additional_settings=additional_settings) != "STRING"


def test_get_artist(album):
    assert isinstance(album.artist, Artist)
