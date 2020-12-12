from buisness_logic.dto import ArtistDto
from buisness_logic.entities._base import SaveSpotifyObjectMixIn


class Artist(SaveSpotifyObjectMixIn):

    def __init__(self, artist_name: str):
        self._save_spotify()

        self._init_instance(artist_name)

    def _init_instance(self, artist_name):
        self._instance = ArtistDto(
            name=artist_name
        )
        self._update_instance()

    @property
    def name(self) -> str:
        return self._instance.name

    def _update_instance(self):
        self._instance = ArtistDto(self.name)
