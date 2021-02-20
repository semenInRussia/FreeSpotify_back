import pytest

from music_manger.implementations.RocknationAndSpotify.spotify import Spotify


@pytest.fixture()
def spotify():
    return Spotify()
