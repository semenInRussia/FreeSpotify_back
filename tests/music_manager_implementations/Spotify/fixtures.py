import pytest

from FreeSpotify_back.music_manager.implementations import Spotify


@pytest.fixture()
def spotify():
    return Spotify()
