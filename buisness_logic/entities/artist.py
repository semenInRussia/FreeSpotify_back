from typing import NamedTuple, List

from buisness_logic.entities._base import SaveSpotifyObjectMixIn


class BaseArtist(NamedTuple):
    artist_name: str

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.artist_name


class Artist(SaveSpotifyObjectMixIn, BaseArtist):
    from buisness_logic.entities.track import Track

    @property
    def name(self):
        return self._get_artist_info()["artist_name"]

    def _get_artist_info(self) -> dict:
        artists_info = self._spotify.get_artists_ids_and_names(self.artist_name)

        return artists_info[0]

    def get_top(self) -> List[Track]:
        top = self._spotify.get_top_music_info_by_approximate_artist_title(self.name)

        return top
