from FreeSpotify_back.music_manager import AbstractMusicManager

from ._albums import DirectoryAlbumsManager
from ._artists import DirectoryArtistsManager
from ._tracks import DirectoryTracksManager


class DirectoryMusicManager(AbstractMusicManager):
    def __init__(self, path: str):
        self._path = path
        self.artists = DirectoryArtistsManager(self._path)
        self.albums = DirectoryAlbumsManager(self._path)
        self.tracks = DirectoryTracksManager(self._path)
