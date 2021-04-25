import pytest

from dto import AlbumDto, TrackDto
from music_manger.implementations.directory_music_manager.directory_music_manager import DirectoryMusicManager
from music_manger.music_manger import AbstractMusicManager
from tests.testdata import path_to_music


@pytest.fixture()
def directory_music_manager():
    return DirectoryMusicManager(path_to_music)


def test_get_album(directory_music_manager: AbstractMusicManager):
    excepted = directory_music_manager.albums.get("artist1", "album1")

    assert isinstance(excepted, AlbumDto)
    assert "album1" == excepted.name


def test_search_albums(directory_music_manager: AbstractMusicManager):
    excepted = directory_music_manager.albums.search("artist2", "album1")

    assert excepted[0] == AlbumDto(artist_name="artist2", name="album1")


def test_tracks_of_album(directory_music_manager: AbstractMusicManager):
    tracks = directory_music_manager.albums.get_tracks("artist1", "album1")

    assert isinstance(tracks, list)

    for track in tracks:
        assert isinstance(track, TrackDto)
