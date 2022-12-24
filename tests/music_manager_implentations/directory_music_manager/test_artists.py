import os

import pytest

from FreeSpotify_back.dto import AlbumDto
from FreeSpotify_back.dto import ArtistDto

from FreeSpotify_back.music_manager.implementations import DirectoryMusicManager
from FreeSpotify_back.music_manager import AbstractMusicManager

from ...testing_data import path_to_music


@pytest.fixture()
def directory_music_manager():
    return DirectoryMusicManager(path_to_music)


def test_get_artist(directory_music_manager: AbstractMusicManager):
    artist = directory_music_manager.artists.get("artist1")

    assert isinstance(artist, ArtistDto)
    assert artist.name == "artist1"

    artist2 = directory_music_manager.artists.get("artist2")

    assert isinstance(artist2, ArtistDto)
    assert artist2.name == "artist2"


def test_search(directory_music_manager: AbstractMusicManager):
    artists = directory_music_manager.artists.search("artist1")

    assert isinstance(artists, list)

    assert artists[0] == ArtistDto(name="artist1")


def test_get_link(directory_music_manager: DirectoryMusicManager):
    assert directory_music_manager.artists.get_link("artist 1") == os.path.join(path_to_music, "artist1")


def test_get_albums(directory_music_manager: DirectoryMusicManager):
    actual = directory_music_manager.artists.get_albums("artist 1")

    assert actual == [AlbumDto("artist1", "album1")]
