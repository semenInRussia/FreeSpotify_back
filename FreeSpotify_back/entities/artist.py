from collections.abc import Iterable
from typing import Optional

from FreeSpotify_back.dto import AlbumDto, ArtistDto, TrackDto
from FreeSpotify_back.music_manager import AbstractMusicManager
from FreeSpotify_back.music_manager.core.exceptions import NotFoundArtistError
from FreeSpotify_back.settings.entities import entities

from ._AbstractEntity import AbstractEntity


class Artist(AbstractEntity):
    """Representation of a music artist.

    It uses a back-end to fetch the information about the artist, so there is
    not fetching, here just a useful API
    """

    _instance: ArtistDto

    def __init__(self, artist_name: str, additional_settings=None):
        """Build an Artist with given parameters.

        If additional_setting provided, then use it.
        """
        self._init_settings(additional_settings)
        self._init_instance(artist_name)
        super().__init__(additional_settings=additional_settings)

    def _init_instance(self, artist_name: str) -> None:
        self._instance = self._music_mgr.artists.get(artist_name)

    def __repr__(self):
        return repr(self._instance)

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.name == other.name

    @property
    def name(self) -> str:
        """Return the name of the artist."""
        return self._instance.name

    @property
    def top(self) -> Iterable:
        """Return the album top tracks."""
        tracks_dto_top = self._music_mgr.artists.get_top(self.name)
        return self._get_top_from_dto_top(tracks_dto_top)

    def _get_top_from_dto_top(self, track_dto_top: Iterable[TrackDto]):
        from . import Track

        for dto_track in track_dto_top:
            yield Track.create_from_dto_or_none(
                dto_track, additional_settings=self.settings
            )

    @property
    def albums(self):
        """Return the artist albums."""
        dto_albums = self._music_mgr.artists.get_albums(self.name)
        return self._get_albums_from_dto_albums(dto_albums)

    def _get_albums_from_dto_albums(self, dto_albums: Iterable[AlbumDto]):
        from . import Album

        for dto_album in dto_albums:
            yield Album.create_from_dto(dto_album, additional_settings=self.settings)

    @property
    def link(self) -> Optional[str]:
        """Return the link to download the artist tracks."""
        try:
            return self._music_mgr.artists.get_link(self._instance.name)
        except NotFoundArtistError:
            return None

    @property
    def link_on_img(self) -> Optional[str]:
        """Return the link to artist image."""
        try:
            return self._music_mgr.artists.get_link_on_img(self.name)
        except NotFoundArtistError:
            return None

    @classmethod
    def create_from_dto(cls, dto: ArtistDto, additional_settings=None) -> "Artist":
        """Create an `Artist` from a given `ArtistDto`."""
        return cls(dto.name, additional_settings=additional_settings)

    @staticmethod
    def search(artist_name: str, additional_settings=None) -> Iterable["Artist"]:
        """Return a list which suits with artst_name."""
        return Artist.query(artist_name, additional_settings=additional_settings)

    @staticmethod
    def query(query: str, additional_settings=None) -> Iterable["Artist"]:
        """Return a list which suits with a given query."""
        settings = entities + additional_settings
        music_mgr: AbstractMusicManager = settings.music_manager_impl()
        dtos = music_mgr.artists.query(query)
        return map(Artist.create_from_dto, dtos)

    @classmethod
    def from_query(cls, query: str, additional_settings=None) -> "Artist":
        """Return an `Artist` object that matches with query."""
        try:
            return next(iter(cls.query(query, additional_settings=additional_settings)))
        except StopIteration:
            raise NotFoundArtistError from StopIteration
