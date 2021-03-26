import pytest

from dto import TrackDto
from entities import Album
from entities import Artist
from entities.track import Track
from tests.settigs_for_test import settings_with_mock

artist_name = "Metallica"
album_name = "Master of Puppets"
track_name = "Master of Puppets"

approximate_track_name = "master of puppet"


@pytest.fixture()
def track():
    return Track(
        artist_name=artist_name,
        album_name=album_name,
        track_name=approximate_track_name,

        additional_settings=settings_with_mock
    )

@pytest.fixture()
def track_dto():
    track_dto = TrackDto(
        artist_name=artist_name,
        album_name=album_name,
        name=track_name
    )
    return track_dto


def test_track_artist(track):
    assert isinstance(track.artist, Artist)


def test_work_with_settings(track):
    assert track.settings.music_manager_impl == settings_with_mock.music_manager_impl


def test_track_album(track):
    assert isinstance(track.album, Album)


def test_track_get_name(track):
    assert isinstance(track.name, str)

def test_track_get_disc_number(track: Track):
    assert isinstance(track.disc_number, int)

def test_track_create_from_dto(track_dto: TrackDto):
    track = Track.create_from_dto(track_dto)

    assert isinstance(track, Track)


def test_work_with_settings_when_create_from_dto(track_dto: TrackDto):
    track = Track.create_from_dto(track_dto, additional_settings=settings_with_mock)

    assert settings_with_mock.music_manager_impl == track.settings.music_manager_impl
