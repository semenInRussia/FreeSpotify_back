import pytest

from dto import TrackDto
from entities import Album
from entities import Artist
from entities.track import Track

artist_name = "Metallica"
album_name = "Master of Puppets"
track_name = "Master of Puppets"

approximate_track_name = "master of puppet"


@pytest.fixture
def track():
    return Track(
        artist_name=artist_name,
        album_name=album_name,
        track_name=approximate_track_name
    )


def test_track_artist(track):
    assert isinstance(track.artist, Artist)


def test_track_album(track):
    assert isinstance(track.album, Album)


def test_track_precise_name(track):
    assert isinstance(track.name, str)


def test_track_create_from_dto():
    track_dto = TrackDto(
        artist_name=artist_name,
        album_name=album_name,
        name=track_name
    )

    track = Track.create_from_dto(track_dto)

    assert isinstance(track, Track)


def test_track_get_all_data(track):
    json_data = track.data.get_serialized_data()

    assert 'name' in json_data

    assert 'artist' in json_data
    assert isinstance(json_data.get('artist'), dict)

    assert 'album' in json_data
    assert isinstance(json_data.get('album'), dict)
