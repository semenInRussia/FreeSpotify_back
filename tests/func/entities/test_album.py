from collections import namedtuple

import pytest

from dto import AlbumDto
from entities import Album
from entities.track import Track
from music_manger.implementations import MockMusicManager, RocknationAndSpotify

album_name = "Paranoid"
artist_name = "Black sabbath"

release_date = "1970-09-18"

approximate_album_name = "paranoid  "

num_tracks_in_album = 8

music_manager_impl = MockMusicManager

class settings_with_mock:
    music_manager_impl = music_manager_impl

@pytest.fixture
def album():
    return Album(artist_name, album_name, settings=settings_with_mock)


def test_name(album):
    assert isinstance(album.name, str)

def test_work_with_settings(album):
    assert album.settings.music_manager_impl == music_manager_impl

def test_release_year(album):
    assert isinstance(album.release_date, str)


def test_create_from_dto():
    dto = AlbumDto(artist_name, album_name)

    album = Album.create_from_dto(dto)

    assert isinstance(album, Album)


def test_get_tracks(album):
    tracks = album.tracks

    assert isinstance(tracks[0], Track)
    assert len(tracks)


def test_get_link(album):
    assert isinstance(album.link, str)


def test_get_link_on_img(album):
    assert isinstance(album.link_on_img, str)

