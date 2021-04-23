from typing import List

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
        similar_artist_names = my_os.dirs_similar_to(artist_name, self._path_to_all_artists)
        artists = self._get_artists_from_names(similar_artist_names)

        return artists

    @staticmethod
    def _get_artists_from_names(similar_artist_names) -> List[ArtistDto]:
        return list(map(
            lambda name: ArtistDto(name),
            similar_artist_names
        ))
