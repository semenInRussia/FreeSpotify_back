from typing import Iterable
from typing import Optional

from FreeSpotify_back.settings.entities import entities
from FreeSpotify_back.music_manager import AbstractMusicManager

from ..dto import TrackDto

from ._AbstractEntity import AbstractEntity

from ..music_manager.core.exceptions import NotFoundAlbumException
from ..music_manager.core.exceptions import NotFoundArtistException
from ..music_manager.core.exceptions import NotFoundTrackException


class Track(AbstractEntity):
    _instance: TrackDto

    def __init__(self,
                 artist_name: str,
                 album_name: str,
                 track_name: str,
                 additional_settings=None):
        self._init_settings(additional_settings)
        self._init_instance(artist_name, album_name, track_name)
        super().__init__(additional_settings=additional_settings)

    def _init_instance(self,
                       artist_name: str,
                       album_name: str,
                       track_name: str):
        self._instance = self._music_mgr.tracks.get(
            artist_name=artist_name,
            album_name=album_name,
            track_name=track_name
        )

    def __repr__(self):
        return repr(self._instance)

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__) and
            self.album == other.album and self.name == other.name)

    @classmethod
    def create_from_dto(cls, track_dto: TrackDto, additional_settings=None):
        return cls(
            track_dto.artist_name,
            track_dto.album_name,
            track_dto.name,
            additional_settings=additional_settings,
        )

    @classmethod
    def create_from_dto_or_none(cls,
                                track_dto: TrackDto,
                                additional_settings=None):
        try:
            actual_track = cls.create_from_dto(track_dto,
                additional_settings=additional_settings)
        except (NotFoundTrackException,
                NotFoundAlbumException,
                NotFoundArtistException):
            return None
        else:
            return actual_track

    @property
    def name(self) -> str:
        return self._instance.name

    @property
    def disc_number(self) -> Optional[int]:
        return self._instance.disc_number

    @property
    def artist(self):
        from .artist import Artist

        return Artist(
            self._instance.artist_name,
            additional_settings=self.settings)

    @property
    def album(self):
        from .album import Album

        return Album(self._instance.artist_name,
                     self._instance.album_name,
                     additional_settings=self.settings)

    @property
    def link(self) -> Optional[str]:
        try:
            link = self._music_mgr.tracks.get_link(
                self._instance.artist_name,
                self._instance.album_name,
                self._instance.name)
        except (NotFoundTrackException, NotFoundAlbumException):
            return None
        else:
            return link


    @staticmethod
    def search(artist_name: str,
               album_name: str,
               track_name: str,
               additional_settings=None) -> Iterable["Track"]:
        settings = entities + additional_settings
        music_mgr: AbstractMusicManager = settings.music_manager_impl()
        dtos = music_mgr.tracks.search(artist_name, album_name, track_name)
        return map(Track.create_from_dto, dtos)

    @staticmethod
    def query(query: str, additional_settings=None) -> Iterable["Track"]:
        settings = entities + additional_settings
        music_mgr: AbstractMusicManager = settings.music_manager_impl()
        dtos = music_mgr.tracks.query(query)
        return map(Track.create_from_dto, dtos)

    @classmethod
    def from_query(cls, query: str, additional_settings=None):
        try:
            return next(iter(
                cls.query(query, additional_settings=additional_settings)))
        except StopIteration:
            raise NotFoundTrackException
