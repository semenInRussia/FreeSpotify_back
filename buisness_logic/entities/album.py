from buisness_logic.dto import AlbumDto
from buisness_logic.entities._base import SaveSpotifyObjectMixIn


class Album(SaveSpotifyObjectMixIn):
    def __init__(self, album_name: str, artist_name: str, *args, **kwargs):
        self._save_spotify()

        self._instance = AlbumDto(
            artist_name=artist_name,
            name=album_name
        )

        self._update_instance()

    @property
    def artist(self):
        from buisness_logic.entities.artist import Artist

        return Artist(self._instance.artist_name)

    @property
    def name(self):
        return self._instance.name

    def _update_instance(self):
        self._instance = self._spotify.albums.get(
            self._instance.artist_name,
            self._instance.name
        )
