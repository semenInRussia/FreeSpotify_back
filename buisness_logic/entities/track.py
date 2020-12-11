from typing import NamedTuple

from buisness_logic.entities._base import SaveSpotifyObjectMixIn
from buisness_logic.entities.album import Album


class BaseTrack(NamedTuple):
    track_name: str
    artist_name: str
    album_name: str

    release_date: str = None
    disc_number: int = None
    top_number: int = None

    def __str__(self):
        return f"{self.artist_name} - {self.disc_number}.{self.track_name}"

    def __repr__(self):
        return self.__str__()


class Track(SaveSpotifyObjectMixIn, BaseTrack):
    _name = None

    def __init__(self, precise_data: bool= False, *args, **kwargs):
        super().__init__(args, kwargs)
        self._precise_date = precise_data

    @property
    def name(self):
        if self._precise_date:
            self._update_info()

        return self.artist_name

    @property
    def artist(self):
        from buisness_logic.entities.artist import Artist

        return Artist(self.artist_name)

    @property
    def album(self):
        return Album(self.artist_name, self.album_name)

    def _update_info(self):
        track = self._spotify.get_track_info(self.artist_name, self.track_name)

        self._name = track.artist_name
