from typing import List

import my_os
from dto import AlbumDto
from music_manger.music_manger import AbstractAlbums

RATIO_OF_SIMILARITY_OF_ALBUMS = 0.5


class DirectoryAlbumsManager(AbstractAlbums):
    def __init__(self, path_to_music: str):
        self._path = path_to_music

    def search(self, artist_name: str, album_name: str) -> List[AlbumDto]:
        paths_to_albums = self._search_paths_to_albums(artist_name, album_name)
        albums = self._get_albums_by_paths(paths_to_albums)

        return albums

    def _search_paths_to_albums(self, artist_name: str, album_name: str) -> List[str]:
        return my_os.search_dirs_by_pattern(
            f"{self._path_to_artists}/~{artist_name}/~{album_name}"
        )

    @property
    def _path_to_artists(self):
        return self._path

    def _get_albums_by_paths(self, paths_to_albums: List[str]) -> List[AlbumDto]:
        return list(map(
            self._get_album_by_path,

            paths_to_albums
        ))

    @staticmethod
    def _get_album_by_path(path: str) -> AlbumDto:
        parts_of_paths = my_os.get_parts_of_path(path)

        artist_name = parts_of_paths[-2]
        name = parts_of_paths[-1]

        return AlbumDto(name=name, artist_name=artist_name)

