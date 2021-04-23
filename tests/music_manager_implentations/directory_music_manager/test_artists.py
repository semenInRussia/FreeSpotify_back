import os

import pytest

from dto import ArtistDto
from music_manger.implementations.directory_music_manager.directory_music_manager import DirectoryMusicManager
from music_manger.music_manger import AbstractMusicManager
from tests.music_manager_implentations.directory_music_manager.testdata import path_to_music


@pytest.fixture()
def directory_music_manager():
    return DirectoryMusicManager(path_to_music)


def test_get_artist(directory_music_manager: AbstractMusicManager):
    artist = directory_music_manager.artists.get("artist1")

    assert isinstance(artist, ArtistDto)
    assert "artist1" == artist.name

    artist2 = directory_music_manager.artists.get("artist2")

    assert isinstance(artist2, ArtistDto)
    assert "artist2" == artist2.name


def test_search(directory_music_manager: AbstractMusicManager):
    artists = directory_music_manager.artists.search("artist1")

    assert isinstance(artists, list)

    assert artists[0] == ArtistDto(name="artist1")

def test_get_link(directory_music_manager: DirectoryMusicManager):
    assert directory_music_manager.artists.get_link("artist 1") == os.path.join(path_to_music, "artist1")

