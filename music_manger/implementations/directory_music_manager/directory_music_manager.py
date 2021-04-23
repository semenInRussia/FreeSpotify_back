from music_manger.implementations.directory_music_manager._albums import DirectoryAlbumsManager
from music_manger.implementations.directory_music_manager._artists import DirectoryArtistsManager
from music_manger.music_manger import AbstractMusicManager


class DirectoryMusicManager(AbstractMusicManager):
    def __init__(self, path_to_music: str):
        self._path = path_to_music

        self.artists = DirectoryArtistsManager(self._path)
        self.albums = DirectoryAlbumsManager(self._path)
