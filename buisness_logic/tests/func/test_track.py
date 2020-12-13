import pytest

from buisness_logic.dto import TrackDto
from buisness_logic.entities.album import Album
from buisness_logic.entities.artist import Artist
from buisness_logic.entities.track import Track

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
    assert track.name == track_name


def test_track_create_from_dto():
    track_dto = TrackDto(
        artist_name=artist_name,
        album_name=album_name,
        name=track_name
    )

    track = Track.create_from_dto(track_dto)

    assert isinstance(track, Track)
