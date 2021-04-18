from typing import List

from dto import AlbumDto, TrackDto
from entities._AbstractEntity import AbstractEntity
from music_manger.core.exceptions import NotFoundAlbumException


class Album(AbstractEntity):
    _instance: AlbumDto

    def __init__(self, artist_name: str, album_name: str, additional_settings=None):
        self._init_settings(additional_settings)
        self._init_instance(artist_name, album_name)

        super().__init__(additional_settings=additional_settings)

    def _init_instance(self, artist_name, album_name):
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

    def __repr__(self):
        return repr(self._instance)

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.artist == other.artist and self.name == other.name

    @property
    def artist(self):
        from entities import Artist

        return Artist(self._instance.artist_name, additional_settings=self.settings)

    @property
    def tracks(self) -> list:
        dto_tracks = self._get_dto_tracks()
        tracks = self._get_tracks_from_dto_tracks(dto_tracks)

        return tracks

    def _get_tracks_from_dto_tracks(self, dto_tracks: List[TrackDto]) -> list:
        from entities.track import Track
        tracks = []

        for dto_track in dto_tracks:
            track = Track.create_from_dto(dto_track, additional_settings=self.settings)
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
        try:
            return self._music_mgr.albums.get_link(
                self._instance.artist_name,
                self._instance.name
            )
        except NotFoundAlbumException:
            return None

    @property
    def link_on_img(self):
        try:
            return self._music_mgr.albums.get_link_on_img(
                self._instance.artist_name,
                self.name
            )
        except NotFoundAlbumException:
            return None

    @classmethod
    def create_from_dto(cls, dto: AlbumDto, additional_settings=None):
        return cls(
            dto.artist_name,
            dto.name,

            additional_settings=additional_settings
        )
