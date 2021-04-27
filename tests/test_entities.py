import pytest

from entities import Album
from entities import Artist
from entities import Track
from music_manger.implementations import RocknationAndSpotify

artist_name = "Deep purple"
album_name = "Deep Purple in ROCK!"
track_name = "Speed KIIING!"


@pytest.fixture()
def artist():
    return Artist(artist_name)


@pytest.fixture()
def album():
    return Album(artist_name, album_name)


@pytest.fixture()
def track():
    return Track(artist_name, album_name, track_name)


def test_time_of_get_tracks_of_album(album: Album):
    s
