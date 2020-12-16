from dto import TrackDto
from entities._mixins import _Entity
from entities import Album
from entities.data_manager import DataManager, Serializer


class TrackSerializer(Serializer):
    all_fields = ('name', 'artist', 'album',)

    @property
    def artist(self):
        artist = self._object.artist

        return artist.data.get_serialized_data(
            'name', 'link'
        )

    @property
    def album(self):
        album = self._object.album

        return album.data.get_serialized_data(
            'name', 'link', 'link_on_img', 'release_date'
        )


class Track(_Entity):
    def __init__(self, artist_name: str, album_name: str, track_name: str, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._init_instance(album_name, artist_name, track_name)

        self.data = DataManager(self, TrackSerializer)

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
        from entities import Artist

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
        self._instance = self._music_mgr.tracks.get(
            artist_name=self._instance.artist_name,
            track_name=self._instance.name
        )
