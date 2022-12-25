import os

from typing import Optional
from typing import List
from typing import Iterable

from FreeSpotify_back import my_os
from FreeSpotify_back.dto import TrackDto

from ... import AbstractTracks

EXTENSION_OF_TRACK_FILE = '.mp3'


class DirectoryTracksManager(AbstractTracks):
    def __init__(self, path: str = ''):
        self._path = path

    def search(self,
               artist_name: str,
               album_name: str,
               track_name: str) -> Iterable[TrackDto]:
        paths_to_tracks = my_os.search_dirs_by_pattern(
            f"{self._path}/~{artist_name}/~{album_name}/~{track_name}")

        tracks = self._tracks_from_paths(paths_to_tracks)

        return tracks

    def _tracks_from_paths(self,
                           paths_to_tracks: List[str]) -> Iterable[TrackDto]:
        return map(self._track_from_path, paths_to_tracks)

    @staticmethod
    def _track_from_path(path_to_track: str) -> TrackDto:
        parts_of_path = my_os.get_parts_of_path(path_to_track)

        track_filename = parts_of_path[-1]
        track_name = my_os.file_without_file_extension(track_filename)

        album_name = parts_of_path[-2]
        artist_name = parts_of_path[-3]

        return TrackDto(
            artist_name=artist_name,
            album_name=album_name,
            name=track_name
        )

    def get_link(self,
                 artist_name: str,
                 album_name: str,
                 track_name: str) -> Optional[str]:
        track = self.get(artist_name, album_name, track_name)
        path = self._path_from_track(track)

        return path

    def _path_from_track(self, track: TrackDto) -> str:
        path = os.path.join(
            self._path,
            track.artist_name,
            track.album_name,
            track.name + EXTENSION_OF_TRACK_FILE
        )

        return path
