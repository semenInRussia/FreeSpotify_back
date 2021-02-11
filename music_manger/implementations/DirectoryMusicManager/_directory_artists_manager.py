import difflib
import os
from typing import List, Union

from dto import ArtistDto
from music_manger.music_manger import AbstractArtists

MIN_RATIO_FOR_FULL_SIMILARITY = 0.9
MIN_RATIO_OF_SIMILARITY_FOR_SEARCHING = 0.5


class DirectoryArtistsManager(AbstractArtists):
    def __init__(self, path: str):
        self.path = path
        super().__init__()

    def search(self, artist_name: str) -> List[ArtistDto]:
        similar_artist_names = self._get_artist_names_similar_to_string(artist_name)

        return list(map(
            lambda name: ArtistDto(name),
            similar_artist_names
        ))

    def _get_artist_names_similar_to_string(self, artist_name: str) -> List[str]:
        artist_names = self._get_artist_names()

        return self._get_actual_strings_similar_to_excepted(artist_names, artist_name)

    def _get_artist_names(self) -> List[str]:
        for _, artist_names, _ in os.walk(self.path):
            return artist_names

    def _get_actual_strings_similar_to_excepted(
            self,
            actual_strings: List[str],
            expected: str,
            min_ratio_of_similarity=MIN_RATIO_OF_SIMILARITY_FOR_SEARCHING) -> List[str]:
        """
        Get all similar strings from list of strings.

        For example:
    `   >>> _get_actual_strings_similar_to_excepted(["System", "System of a down", "AC/DC"], "system")
        ['System', 'System of a down']
        """

        similar_strings = list(filter(
            lambda actual_string: self._is_similar_strings(actual_string, expected, min_ratio_of_similarity),

            actual_strings,
        ))

        return sorted(
            similar_strings,
            key=lambda actual_string: self._get_ratio_of_similarity(actual_string, expected)
        )

    def _is_similar_strings(self, actual: str, expected: str, min_ratio=MIN_RATIO_FOR_FULL_SIMILARITY) -> bool:
        """Is similar actual string to excepted string?"""
        ratio = self._get_ratio_of_similarity(actual, expected)

        return ratio > min_ratio

    @staticmethod
    def _get_ratio_of_similarity(actual: str, expected: str) -> float:
        matcher = difflib.SequenceMatcher(None, actual.lower(), expected.lower())

        return matcher.ratio()

    def _find_similar_string_from_list(self,
                                       actual_strings: List[str],
                                       excepted_string: str,
                                       min_ratio=None
                                       ) -> Union[str, None]:
        """
        Find actual string from list actual string

        For example:
        >>> _find_actual_string(["AC/DC", "Black Sabbath", "Pink Floyd"], "ac dc")
        'AC/DC'
        """
        for actual_string in actual_strings:
            if self._is_similar_strings(actual_string, excepted_string, min_ratio):
                return actual_string

    def _get_precise_artist_name(self, artist_name: str) -> str:
        artist_names = self._get_artist_names()

        precise_artist_name = self._find_similar_string_from_list(artist_names, artist_name)

        return precise_artist_name
