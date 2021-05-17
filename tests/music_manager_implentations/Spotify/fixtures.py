import pytest

from music_manger.implementations.rocknation_and_spotify.spotify import Spotify


@pytest.fixture()
def spotify():
    return Spotify()
