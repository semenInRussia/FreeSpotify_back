import pytest

from dto import ArtistDto
from music_manger.implementations.DirectoryMusicManager.directory_music_manager import DirectoryMusicManager
from music_manger.music_manger import AbstractMusicManager

path_to_music = r"C:\Users\Asus\PycharmProjects\FreeSpotify_back\tests\func\music_manager_implentations\directory_music_manager\music"


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
