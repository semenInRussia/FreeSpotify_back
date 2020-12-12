from buisness_logic.dto import TrackDto
from buisness_logic.entities._base import SaveSpotifyObjectMixIn
from buisness_logic.entities.album import Album


class Track(SaveSpotifyObjectMixIn):
    _name = None

    def __init__(self, artist_name: str, album_name: str, track_name: str):
        self._save_spotify()

        self._instance = TrackDto(
            artist_name=artist_name,
            album_name=album_name,
            name=track_name
        )

    @property
    def name(self):
        return self._instance.name

    @property
    def artist(self):
        from buisness_logic.entities.artist import Artist

        return Artist(self._instance.artist_name)

    @property
    def album(self):
        return Album(self._instance.artist_name, self._instance.album_name)
