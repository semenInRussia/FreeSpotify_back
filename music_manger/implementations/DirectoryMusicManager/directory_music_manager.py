from music_manger.implementations.DirectoryMusicManager._directory_albums_manager import DirectoryAlbumsManager
from music_manger.implementations.DirectoryMusicManager._directory_artists_manager import DirectoryArtistsManager
from music_manger.music_manger import AbstractMusicManager


class DirectoryMusicManager(AbstractMusicManager):
    def __init__(self, path_to_music: str):
        self._path = path_to_music

        self.artists = DirectoryArtistsManager(self._path)
        self.albums = DirectoryAlbumsManager(self._path)
