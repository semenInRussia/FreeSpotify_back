from typing import Optional
from typing import List
from typing import Iterable

from ..dto import AlbumDto
from ..dto import ArtistDto

from ._AbstractEntity import AbstractEntity
from ..music_manager.core.exceptions import NotFoundArtistException

from FreeSpotify_back.settings.entities import entities
from ..music_manager import AbstractMusicManager


class Artist(AbstractEntity):
    _instance: ArtistDto

    def __init__(self, artist_name: str, additional_settings=None):
        self._init_settings(additional_settings)
        self._init_instance(artist_name)

        super().__init__(additional_settings=additional_settings)

    def _init_instance(self, artist_name):
        self._instance = self._music_mgr.artists.get(artist_name)

    def __repr__(self):
        return repr(self._instance)

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.name == other.name

    @property
    def name(self) -> str:
        return self._instance.name

    @property
    def top(self):
        tracks_dto_top = self._music_mgr.artists.get_top(self.name)

        tracks_top = self._get_top_from_dto_top(tracks_dto_top)

        return tracks_top

    def _get_top_from_dto_top(self, track_dto_top):
        from . import Track

        for dto_track in track_dto_top:
            yield Track.create_from_dto_or_none(
                dto_track,
                additional_settings=self.settings)

    @property
    def albums(self):
        dto_albums = self._music_mgr.artists.get_albums(self.name)
        albums = self._get_albums_from_dto_albums(dto_albums)

        return albums

    def _get_albums_from_dto_albums(self, dto_albums: List[AlbumDto]):
        from . import Album

        return list(map(
            lambda dto_album: Album.create_from_dto(dto_album, additional_settings=self.settings),

            dto_albums
        ))

    @property
    def link(self) -> Optional[str]:
        try:
            return self._music_mgr.artists.get_link(self._instance.name)
        except NotFoundArtistException:
            return None

    @property
    def link_on_img(self):
        try:
            return self._music_mgr.artists.get_link_on_img(
                self.name
            )
        except NotFoundArtistException:
            return None

    @classmethod
    def create_from_dto(cls, dto: ArtistDto, additional_settings=None):
        return cls(
            dto.name,

            additional_settings=additional_settings
        )

    @staticmethod
    def search(artist_name: str,
               additional_settings=None) -> Iterable["Artist"]:
        return Artist.query(artist_name,
                            additional_settings=additional_settings)

    @staticmethod
    def query(query: str, additional_settings=None) -> Iterable["Artist"]:
        settings = entities + additional_settings
        music_mgr: AbstractMusicManager = settings.music_manager_impl()
        dtos = music_mgr.artists.query(query)
        return map(Artist.create_from_dto, dtos)

    @classmethod
    def from_query(cls, query: str, additional_settings=None):
        try:
            return next(iter(
                cls.query(query, additional_settings=additional_settings)))
        except StopIteration:
            raise NotFoundArtistException
