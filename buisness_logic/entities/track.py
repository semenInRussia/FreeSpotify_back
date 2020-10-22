from typing import NamedTuple

from buisness_logic.entities._base import SaveSpotifyObjectMixIn
from buisness_logic.entities.album import Album


class BaseTrack(SaveSpotifyObjectMixIn, NamedTuple):
    track_name: str
    artist_name: str
    album_name: str

    release_date: str = None
    disc_number: int = None
    top_number: int = None

    def __str__(self):
        return f"{self.artist_name} - {self.disc_number}. {self.track_name}"

    def __repr__(self):
        return self.__str__()


class Track(BaseTrack):
    @property
    def name(self):
        from buisness_logic.spotifyPythonAPI import get_track_info

        track_info = get_track_info(self.artist_name, self.track_name, self._spotify)

        return track_info["name"]

    @property
    def artist(self):
        from buisness_logic.entities.artist import Artist

        return Artist(self.artist_name)

    @property
    def album(self):
        return Album(self.artist_name, self.album_name)
