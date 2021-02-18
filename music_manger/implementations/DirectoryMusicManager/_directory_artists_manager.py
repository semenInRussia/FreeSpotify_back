import os
from typing import List

from dto import ArtistDto
from music_manger.music_manger import AbstractArtists
from similarity_lib import \
    filter_and_sort_strings_by_min_similarity_to


class DirectoryArtistsManager(AbstractArtists):
    def __init__(self, path: str):
        self.path = path

        super().__init__()

    def search(self, artist_name: str) -> List[ArtistDto]:
        similar_artist_names = self._get_filtered_artist_names_by_similarity_to(artist_name)

        return self._get_artists_from_names(similar_artist_names)

    def _get_filtered_artist_names_by_similarity_to(self, artist_name: str) -> List[str]:
        artist_names = self._get_all_artist_names()
        filtered_artist_names = filter_and_sort_strings_by_min_similarity_to(artist_name, artist_names)

        return filtered_artist_names

    def _get_all_artist_names(self) -> List[str]:
        for _, artist_names, _ in os.walk(self.path):
            return artist_names

    def _get_artists_from_names(self, similar_artist_names) -> List[ArtistDto]:
        return list(map(
            lambda name: ArtistDto(name),
            similar_artist_names
        ))
