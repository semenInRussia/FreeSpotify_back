from buisness_logic.dto import AlbumDto
from buisness_logic.entities._base import SaveSpotifyObjectMixIn


class Album(SaveSpotifyObjectMixIn):
    def __init__(self, album_name: str, artist_name: str):
        self._save_spotify()

        self._instance = AlbumDto(
            artist_name=artist_name,
            name=album_name
        )

        self._update_instance()

    def _update_instance(self):
        self._instance = self._spotify.albums.get(
            self._instance.artist_name,
            self._instance.name
        )

    @property
    def artist(self):
        from buisness_logic.entities.artist import Artist

        return Artist(self._instance.artist_name)

    @property
    def name(self) -> str:
        return self._instance.name

    @property
    def release_date(self) -> str:
        return self._instance.release_date

    @classmethod
    def create_from_dto(cls, dto: AlbumDto):
        return cls(
            dto.artist_name,
            dto.name
        )
