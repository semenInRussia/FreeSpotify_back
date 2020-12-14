from dto import ArtistDto
from entities._mixins import SaveSpotifyObjectMixIn


class Artist(SaveSpotifyObjectMixIn):

    def __init__(self, artist_name: str):
        self._save_spotify()

        self._init_instance(artist_name)

    def _init_instance(self, artist_name):
        self._instance = ArtistDto(
            name=artist_name
        )
        self._update_instance()

    def _update_instance(self):
        self._instance = self._spotify.artists.get(self.name)

    @property
    def name(self) -> str:
        return self._instance.name

    @property
    def top(self):
        track_dto_top = self._spotify.artists.get_top(self.name)

        track_top = self._get_top_from_dto_top(track_dto_top)

        return track_top

    def _get_top_from_dto_top(self, track_dto_top):
        from entities.track import Track

        top = []

        for dto_track in track_dto_top:
            track = Track.create_from_dto(dto_track)

            top.append(track)

        return top

    @classmethod
    def create_from_dto(cls, dto):
        return cls(
            dto.name
        )