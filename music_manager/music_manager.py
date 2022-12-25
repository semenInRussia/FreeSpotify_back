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

    def query(self, query: str) -> Iterable[ArtistDto]:
        # you should implemet method `query` or `search` or both
        return self.search(query)

    def search(self, artist_name: str) -> Iterable[ArtistDto]:
        # you should implemet method `query` or `search` or both
        return self.query(artist_name)

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

    def query(self, query: str) -> Iterable[AlbumDto]:
        # you should implemet method `query` or `search` or both
        artist_name, album_name = query.split(" - ")
        return self.search(artist_name, album_name)

    def search(self, artist_name: str, album_name: str) -> Iterable[AlbumDto]:
        # you should implemet method `query` or `search` or both
        query = artist_name + " - " + album_name
        return self.query(query)

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

    def query(self, query: str) -> Iterable[TrackDto]:
        # you should implemet method `query` or `search` or both
        artist_name, track_name = query.split(" - ")
        return self.search(artist_name, "", track_name)

    def search(self,
               artist_name: str,
               _album_name: str,
               track_name: str) -> Iterable[TrackDto]:
        # you should implemet method `query` or `search` or both
        query = artist_name + " - " + track_name
        return self.query(query)

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
