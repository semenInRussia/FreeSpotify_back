from typing import NamedTuple

from buisness_logic.entities._base import SaveSpotifyObjectMixIn
from buisness_logic.spotifyPythonAPI import get_artists_ids_and_names


class BaseArtist(NamedTuple):
    artist_name: str

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.artist_name


class Artist(SaveSpotifyObjectMixIn, BaseArtist):
    @property
    def name(self):
        return self._get_artist_info()["artist_name"]

    def _get_artist_info(self) -> dict:
        artists_info = get_artists_ids_and_names(self.artist_name, self._spotify)

        return artists_info[0]

    def get_top(self):
        pass
