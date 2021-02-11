import difflib
import os
from typing import List, Union

from dto import ArtistDto
from music_manger.music_manger import AbstractArtists

MIN_RATIO_FOR_EQUAL_STRING = 0.9

class DirectoryArtistsManager(AbstractArtists):
    def __init__(self, path: str):
        self.path = path
        super().__init__()

    def get(self, artist_name: str) -> ArtistDto:
        precise_artist_name = self._get_precise_artist_name(artist_name)

        return ArtistDto(precise_artist_name)

    def _get_precise_artist_name(self, artist_name: str) -> str:
        for _, dirs_names, _ in os.walk(self.path):
            precise_artist_name = self._find_actual_string_from_list(dirs_names, artist_name)

            return precise_artist_name

    def _find_actual_string_from_list(self, actual_strings: List[str], excepted_string: str) -> Union[str, None]:
        """
        Find actual string from list actual string

        For example:
        >>> _find_actual_string(["AC/DC", "Black Sabbath", "Pink Floyd"], "ac dc")
        'AC/DC'
        """
        for actual_string in actual_strings:
            if self._is_similar_strings(actual_string, excepted_string):
                return actual_string

    @staticmethod
    def _is_similar_strings(actual: str, expected: str, min_ratio=MIN_RATIO_FOR_EQUAL_STRING) -> bool:
        matcher = difflib.SequenceMatcher(None, actual.lower(), expected.lower())

        return matcher.ratio() > min_ratio
