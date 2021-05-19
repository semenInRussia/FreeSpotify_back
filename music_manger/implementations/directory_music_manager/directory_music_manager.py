from music_manger.implementations.directory_music_manager._albums import DirectoryAlbumsManager
from music_manger.implementations.directory_music_manager._artists import DirectoryArtistsManager
from music_manger.implementations.directory_music_manager._tracks import DirectoryTracksManager
from music_manger.music_manger import AbstractMusicManager


class DirectoryMusicManager(AbstractMusicManager):
    def __init__(self, path: str):
        self._path = path

        self.artists = DirectoryArtistsManager(self._path)
        self.albums = DirectoryAlbumsManager(self._path)
        self.tracks = DirectoryTracksManager(self._path)
