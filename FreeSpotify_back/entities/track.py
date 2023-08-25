from collections.abc import Iterable
from typing import Optional

from FreeSpotify_back.dto import TrackDto
from FreeSpotify_back.music_manager import AbstractMusicManager
from FreeSpotify_back.music_manager.core.exceptions import (
    NotFoundAlbumError,
    NotFoundArtistError,
    NotFoundTrackError,
)
from FreeSpotify_back.settings.entities import entities

from ._AbstractEntity import AbstractEntity


class Track(AbstractEntity):
    """Representation of a music track.

    It uses a back-end to fetch the information about the track, so there is
    not fetching, here just a useful API
    """

    _instance: TrackDto

    def __init__(
        self,
        artist_name: str,
        album_name: str,
        track_name: str,
        additional_settings=None,
    ):
        """Build a Track with given parameters.

        If additional_setting provided, then use it.
        """
        self._init_settings(additional_settings)
        self._init_instance(artist_name, album_name, track_name)
        super().__init__(additional_settings=additional_settings)

    def _init_instance(
        self, artist_name: str, album_name: str, track_name: str
    ) -> None:
        self._instance = self._music_mgr.tracks.get(
            artist_name=artist_name,
            album_name=album_name,
            track_name=track_name,
        )

    def __repr__(self):
        return repr(self._instance)

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__)
            and self.album == other.album
            and self.name == other.name
        )

    @classmethod
    def create_from_dto(cls, track_dto: TrackDto, additional_settings=None) -> "Track":
        """Construct a new Track object from a given `TrackDto`."""
        return cls(
            track_dto.artist_name,
            track_dto.album_name,
            track_dto.name,
            additional_settings=additional_settings,
        )

    @classmethod
    def create_from_dto_or_none(
        cls, track_dto: TrackDto, additional_settings=None
    ) -> Optional["Track"]:
        """Like ok `create_from_dto`, but if it raise an error, return None."""
        try:
            actual_track = cls.create_from_dto(
                track_dto, additional_settings=additional_settings
            )
        except (NotFoundTrackError, NotFoundAlbumError, NotFoundArtistError):
            return None
        else:
            return actual_track

    @property
    def name(self) -> str:
        """Return the track name."""
        return self._instance.name

    @property
    def disc_number(self) -> Optional[int]:
        """Reuturn either the track number on disc or None."""
        return self._instance.disc_number

    @property
    def artist(self):
        """Return the artist of the track (use Artist object)."""
        from .artist import Artist

        return Artist(self._instance.artist_name, additional_settings=self.settings)

    @property
    def album(self):
        """Return the album of the track."""
        from .album import Album

        return Album(
            self._instance.artist_name,
            self._instance.album_name,
            additional_settings=self.settings,
        )

    @property
    def link(self) -> Optional[str]:
        """Return either the URL to download the track or None."""
        try:
            link = self._music_mgr.tracks.get_link(
                self._instance.artist_name,
                self._instance.album_name,
                self._instance.name,
            )
        except (NotFoundTrackError, NotFoundAlbumError):
            return None
        else:
            return link

    @property
    def link_on_img(self) -> Optional[str]:
        """Return the URL to the track image."""
        return self.album.link_on_img

    @staticmethod
    def search(
        artist_name: str, album_name: str, track_name: str, additional_settings=None
    ) -> Iterable["Track"]:
        """Return a list of the tracks that matched with given parameters."""
        settings = entities + additional_settings
        music_mgr: AbstractMusicManager = settings.music_manager_impl()
        dtos = music_mgr.tracks.search(artist_name, album_name, track_name)
        return map(Track.create_from_dto, dtos)

    @staticmethod
    def query(query: str, additional_settings=None) -> Iterable["Track"]:
        """Return a list of the tracks that matched with a given query."""
        settings = entities + additional_settings
        music_mgr: AbstractMusicManager = settings.music_manager_impl()
        dtos = music_mgr.tracks.query(query)
        return map(Track.create_from_dto, dtos)

    @classmethod
    def from_query(cls, query: str, additional_settings=None) -> "Track":
        """Fetch an album from the query."""
        try:
            return next(iter(cls.query(query, additional_settings=additional_settings)))
        except StopIteration:
            raise NotFoundTrackError from StopIteration
