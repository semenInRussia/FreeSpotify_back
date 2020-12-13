from buisness_logic.dto import TrackDto
from buisness_logic.entities._base import SaveSpotifyObjectMixIn
from buisness_logic.entities.album import Album


class Track(SaveSpotifyObjectMixIn):
    def __init__(self, artist_name: str, album_name: str, track_name: str):
        self._save_spotify()

        self._init_instance(album_name, artist_name, track_name)

    def _init_instance(self, album_name, artist_name, track_name):
        self._instance = TrackDto(
            artist_name=artist_name,
            album_name=album_name,
            name=track_name
        )
        self._update_instance()

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

    @classmethod
    def create_from_dto(cls, track_dto: TrackDto):
        return cls(
            track_dto.artist_name,
            track_dto.album_name,
            track_dto.name
        )

    def _update_instance(self):
        self._instance = self._spotify.tracks.get(
            artist_name=self._instance.artist_name,
            track_name=self.name
        )
