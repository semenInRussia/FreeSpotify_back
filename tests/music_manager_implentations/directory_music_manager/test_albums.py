import os

import pytest

from dto import AlbumDto
from dto import TrackDto
from music_manger.implementations.directory_music_manager.directory_music_manager import DirectoryMusicManager
from music_manger.music_manger import AbstractMusicManager
from tests.testing_data import path_to_music


@pytest.fixture()
def directory_music_manager():
    return DirectoryMusicManager(path_to_music)


def test_get_album(directory_music_manager: AbstractMusicManager):
    excepted = directory_music_manager.albums.get("artist1", "album1")

    assert isinstance(excepted, AlbumDto)
    assert "album1" == excepted.name


def test_search_albums(directory_music_manager: AbstractMusicManager):
    actual = directory_music_manager.albums.search("artist2", "album1")

    assert actual[0] == AlbumDto(artist_name="artist2", name="album1")


def test_get_link(directory_music_manager: AbstractMusicManager):
    actual = directory_music_manager.albums.get_link("artist 1", "1 album")

    assert actual == os.path.join(path_to_music, "artist1", "album1")


def test_tracks_of_album(directory_music_manager: AbstractMusicManager):
    tracks = directory_music_manager.albums.get_tracks("artist1", "album1")

    assert set(tracks) == {
        TrackDto(artist_name="artist1", album_name="album1", name="track1"),
        TrackDto(artist_name="artist1", album_name="album1", name="track2")
    }
