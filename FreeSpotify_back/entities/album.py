from collections.abc import Iterable
from typing import Optional

from FreeSpotify_back.dto import AlbumDto, TrackDto
from FreeSpotify_back.music_manager import AbstractMusicManager
from FreeSpotify_back.music_manager.core.exceptions import NotFoundAlbumError
from FreeSpotify_back.settings.entities import entities

from ._AbstractEntity import AbstractEntity


class Album(AbstractEntity):
    """Representation of a music album.

    It uses a back-end to fetch the information about the album, so there is
    not fetching, here just a useful API.
    """

    _instance: AlbumDto

    def __init__(self,
                 artist_name: str,
                 album_name: str,
                 additional_settings=None):
        """Build an Album with given parameters.

        If additional_setting provided, then use it.
        """
        self._init_settings(additional_settings)
        self._init_instance(artist_name, album_name)
        super().__init__(additional_settings=additional_settings)

    def _init_instance(self, artist_name: str, album_name: str) -> None:
        self._instance = self._music_mgr.albums.get(artist_name,
                                                    album_name)

    def __repr__(self) -> str:
        return repr(self._instance)

    def __eq__(self, other) -> bool:
        return isinstance(other, self.__class__) \
             and self.artist == other.artist and self.name == other.name

    @property
    def artist(self):
        """Return the artist of the album (use Artist object)."""
        from . import Artist

        return Artist(self._instance.artist_name,
                      additional_settings=self.settings)

    @property
    def tracks(self) -> Iterable:
        """Return the list of tracks of the album."""
        dto_tracks = self._get_dto_tracks()
        return self._get_tracks_from_dto_tracks(dto_tracks)

    def _get_dto_tracks(self) -> Iterable[TrackDto]:
        return self._music_mgr.albums.get_tracks(
            self._instance.artist_name,
            self._instance.name,
        )

    def _get_tracks_from_dto_tracks(self,
                                    tracks: Iterable[TrackDto]) -> Iterable:
        return map(self._create_track_from_dto, tracks)

    def _create_track_from_dto(self, dto_track: TrackDto):
        from . import Track

        return Track.create_from_dto(
            dto_track,
            additional_settings=self.settings,
        )

    @property
    def name(self) -> str:
        """Return the name of the album."""
        return self._instance.name

    @property
    def release_date(self) -> Optional[str]:
        """Return either the release date of the album as string or None."""
        return self._instance.release_date

    @property
    def link(self) -> Optional[str]:
        """Return URL to web-page of the album."""
        try:
            return self._music_mgr.albums.get_link(
                self._instance.artist_name,
                self._instance.name,
            )
        except NotFoundAlbumError:
            return None

    @property
    def link_on_img(self) -> Optional[str]:
        """Return either URL to the album image or None."""
        try:
            return self._music_mgr.albums.get_link_on_img(
                self._instance.artist_name,
                self.name,
            )
        except NotFoundAlbumError:
            return None

    @classmethod
    def create_from_dto(cls,
                        dto: AlbumDto,
                        additional_settings=None) -> "Album":
        """Construct a new Album object from a given `AlbumDto`."""
        return cls(
            dto.artist_name,
            dto.name,
            additional_settings=additional_settings,
        )

    @staticmethod
    def search(artist_name: str,
               album_name: str,
               additional_settings=None) -> Iterable["Album"]:
        """Return a list of the albums that matched with given parameters."""
        settings = entities + additional_settings
        music_mgr: AbstractMusicManager = settings.music_manager_impl()
        dtos = music_mgr.albums.search(artist_name, album_name)
        return map(Album.create_from_dto, dtos)

    @staticmethod
    def query(query: str, additional_settings=None) -> Iterable["Album"]:
        """Return a list of the albums that matched with a given queries."""
        settings = entities + additional_settings
        music_mgr: AbstractMusicManager = settings.music_manager_impl()
        dtos = music_mgr.albums.query(query)
        return map(Album.create_from_dto, dtos)

    @classmethod
    def from_query(cls, query: str, additional_settings=None) -> "Album":
        """Fetch an album from the query."""
        try:
            return next(iter(
                cls.query(query, additional_settings=additional_settings)))
        except StopIteration:
            raise NotFoundAlbumError from StopIteration

