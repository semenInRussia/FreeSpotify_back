from dto import AlbumDto
from entities._mixins import _Entity
from entities.data_manager import DataManager, Serializer


class AlbumSerializer(Serializer):
    all_fields = ['name', 'tracks', 'release_date', 'artist', 'link_on_img', 'link']

    @property
    def tracks(self):
        tracks = []

        for track in self._object.tracks:
            tracks.append(
                track.data.get_serialized_data('name')
            )

        return tracks

    @property
    def artist(self):
        artist = self._object.artist

        return artist.data.get_serialized_data(
            'name', 'link'
        )


class Album(_Entity):
    def __init__(self, album_name: str, artist_name: str):
        super().__init__()

        self._init_instance(album_name, artist_name)

        self.data = DataManager(self, AlbumSerializer)

    def _init_instance(self, album_name, artist_name):
        self._instance = AlbumDto(
            artist_name=artist_name,
            name=album_name
        )
        self._update_instance()

    def _update_instance(self):
        self._instance = self._music_mgr.albums.get(
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
        return self._music_mgr.albums.get_tracks(
            self._instance.artist_name,
            self.name
        )

    @property
    def name(self) -> str:
        return self._instance.name

    @property
    def release_date(self) -> str:
        return self._instance.release_date

    @property
    def link(self):
        return self._music_mgr.albums.get_link(
            self._instance.artist_name,
            self._instance.name
        )

    @property
    def link_on_img(self):
        return self._music_mgr.albums.get_link_on_img(
            self._instance.artist_name,
            self.name
        )

    @classmethod
    def create_from_dto(cls, dto: AlbumDto):
        return cls(
            dto.artist_name,
            dto.name
        )
