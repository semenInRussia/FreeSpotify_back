import os
from typing import List

from dto import AlbumDto
import my_os
from dto import ArtistDto
from music_manger.music_manger import AbstractArtists


class DirectoryArtistsManager(AbstractArtists):
    def __init__(self, path: str):
        self.path = path

        super().__init__()

    @property
    def _path_to_all_artists(self) -> str:
        return self.path

    def search(self, artist_name: str) -> List[ArtistDto]:
        artists_paths = my_os.dirs_similar_to(
            artist_name,
            self._path_to_all_artists
        )
        artists = self._get_artists_from_paths(artists_paths)

        return artists

    def _get_artists_from_paths(self, artists_paths: List[str]):
        return list(map(
            self._artist_from_path,
            artists_paths
        ))

    @staticmethod
    def _artist_from_path(path: str):
        parts_of_path = my_os.get_parts_of_path(path)

        artist_name = parts_of_path[-1]

        return ArtistDto(artist_name)

    def get_link(self, artist_name: str) -> str:
        artist = self.get(artist_name)

        return os.path.join(self._path_to_all_artists, artist.name)

    def get_albums(self, artist_name: str) -> List[AlbumDto]:
        path_to_artist = self.get_link(artist_name)
        albums = self._albums_by_path_to_artist(path_to_artist)

        return albums

    def _albums_by_path_to_artist(self, path_to_artist: str) -> List[AlbumDto]:
        album_names = my_os.dirs_names(path_to_artist)
        artist_name = self._artist_from_path(path_to_artist).name

        return list(map(
            lambda album_name: AlbumDto(artist_name, album_name),

            album_names
        ))
