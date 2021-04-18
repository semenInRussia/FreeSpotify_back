from dto import TrackDto
from entities import Album
from entities._AbstractEntity import AbstractEntity


class Track(AbstractEntity):
    _instance: TrackDto

    def __init__(self, artist_name: str, album_name: str, track_name: str, additional_settings=None):
        self._init_settings(additional_settings)
        self._init_instance(artist_name, album_name, track_name)

        super().__init__(additional_settings=additional_settings)

    def _init_instance(self, artist_name: str, album_name: str, track_name: str):
        self._instance = TrackDto(
            artist_name=artist_name,
            album_name=album_name,
            name=track_name
        )

        self._update_instance()

    def _update_instance(self):
        self._instance = self._music_mgr.tracks.get(
            artist_name=self._instance.artist_name,
            album_name=self._instance.album_name,
            track_name=self._instance.name
        )

    def __repr__(self):
        return repr(self._instance)

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.album == other.album and self.name == other.name

    @classmethod
    def create_from_dto(cls, track_dto: TrackDto, additional_settings=None):
        return cls(
            track_dto.artist_name,
            track_dto.album_name,
            track_dto.name,

            additional_settings=additional_settings,
        )

    @property
    def name(self) -> str:
        return self._instance.name

    @property
    def disc_number(self) -> int:
        return self._instance.disc_number

    @property
    def artist(self):
        from entities import Artist

        return Artist(self._instance.artist_name, additional_settings=self.settings)

    @property
    def album(self):
        return Album(self._instance.artist_name, self._instance.album_name, additional_settings=self.settings)
