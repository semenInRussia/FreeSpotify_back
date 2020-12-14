from dto import AlbumDto
from entities._mixins import SaveSpotifyObjectMixIn


class Album(SaveSpotifyObjectMixIn):
    def __init__(self, album_name: str, artist_name: str):
        super().__init__()

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
        from entities import Artist

        return Artist(self._instance.artist_name)

    @property
    def tracks(self) -> list:
        from entities.track import Track

        tracks = []

        dto_tracks = self._get_dto_tracks()

        for dto_track in dto_tracks:
            track = Track.create_from_dto(dto_track)
            tracks.append(track)

        return tracks

    def _get_dto_tracks(self):
        return self._spotify.albums.get_tracks(
            self._instance.artist_name,
            self.name
        )

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
