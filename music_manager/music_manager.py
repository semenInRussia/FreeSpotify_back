from typing import Iterable
from typing import Optional

from ..dto import AlbumDto
from ..dto import ArtistDto
from ..dto import TrackDto

from .core.exceptions import NotFoundAlbumException
from .core.exceptions import NotFoundArtistException
from .core.exceptions import NotFoundTrackException


class AbstractArtists:
    def get(self, artist_name: str) -> ArtistDto:
        try:
            return next(iter(self.search(artist_name)))
        except StopIteration:
            raise NotFoundArtistException

    def search(self, artist_name: str) -> Iterable[ArtistDto]:
        return NotImplemented

    def get_top(self, artist_name: str) -> Iterable[TrackDto]:
        return NotImplemented

    def get_albums(self, artist_name: str) -> Iterable[AlbumDto]:
        return NotImplemented

    def get_link(self, artist_name: str) -> Optional[str]:
        return NotImplemented

    def get_link_on_img(self, artist_name: str) -> Optional[str]:
        return NotImplemented


class AbstractAlbums:
    def get(self, artist_name: str, album_name: str) -> AlbumDto:
        try:
            return next(iter(self.search(artist_name, album_name)))
        except StopIteration:
            raise NotFoundAlbumException

    def search(self, artist_name: str, album_name: str) -> Iterable[AlbumDto]:
        return NotImplemented

    def get_tracks(self,
                   artist_name: str,
                   album_name: str) -> Iterable[TrackDto]:
        return NotImplemented

    def get_link(self, artist_name, album_name: str) -> Optional[str]:
        return NotImplemented

    def get_link_on_img(self,
                        artist_name: str,
                        album_name: str) -> Optional[str]:
        return NotImplemented


class AbstractTracks:
    def get(self,
            artist_name: str,
            album_name: str,
            track_name: str) -> TrackDto:
        try:
            return next(iter(self.search(artist_name, album_name, track_name)))
        except StopIteration:
            raise NotFoundTrackException

    def search(self,
               artist_name: str,
               album_name: str,
               track_name: str) -> Iterable[TrackDto]:
        return NotImplemented

    def get_link(self,
                 artist_name: str,
                 album_name: str,
                 track_name: str) -> Optional[str]:
        return NotImplemented

    def get_link_on_img(self,
                        artist_name: str,
                        album_name: str,
                        track_name: str) -> Optional[str]:
        return NotImplemented


class AbstractMusicManager:
    artists: AbstractArtists
    albums: AbstractAlbums
    tracks: AbstractTracks
