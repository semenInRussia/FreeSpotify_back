import os
from typing import List

from FreeSpotify_back import my_os

from FreeSpotify_back.dto import AlbumDto
from FreeSpotify_back.dto import TrackDto

from ... import AbstractAlbums

RATIO_OF_SIMILARITY_OF_ALBUMS = 0.5


class DirectoryAlbumsManager(AbstractAlbums):
    def __init__(self, path_to_music: str):
        self._path = path_to_music

    def search(self, artist_name: str, album_name: str) -> List[AlbumDto]:
        paths_to_albums = self._search_paths_to_albums(artist_name, album_name)
        albums = self._get_albums_by_paths(paths_to_albums)

        return albums

    def _search_paths_to_albums(
            self,
            artist_name: str,
            album_name: str
    ) -> List[str]:
        return my_os.search_dirs_by_pattern(
            f"{self._path}/~{artist_name}/~{album_name}"
        )

    def _get_albums_by_paths(
            self, paths_to_albums: List[str]) -> List[AlbumDto]:
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

    def get_link(self, artist_name, album_name: str) -> str:
        album = self.get(artist_name, album_name)

        return self._path_from_album(album)

    def _path_from_album(self, album: AlbumDto):
        return os.path.join(
            self._path,
            album.artist_name,
            album.name
        )

    def get_tracks(self, artist_name: str, album_name: str) -> List[TrackDto]:
        album = self.get(artist_name, album_name)
        path_to_album = self._path_from_album(album)

        return list(map(
            lambda track_filename: self._track_from_filename(
                artist_name,
                album_name,
                track_filename
            ),
            my_os.dirs_names(path_to_album)
        ))

    @staticmethod
    def _track_from_filename(
            artist_name: str,
            album_name: str,
            track_filename: str
    ) -> TrackDto:
        track_name = my_os.file_without_file_extension(track_filename)

        return TrackDto(artist_name, album_name, track_name)
