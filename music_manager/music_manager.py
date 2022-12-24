from typing import List
from typing import Type

from ..dto import AlbumDto
from ..dto import ArtistDto
from ..dto import TrackDto

from .core.exceptions import NotFoundAlbumException
from .core.exceptions import NotFoundArtistException
from .core.exceptions import NotFoundTrackException


class AbstractArtists:
    def get(self, artist_name: str) -> ArtistDto:
        try:
            return self.search(artist_name)[0]
        except IndexError:
            raise NotFoundArtistException

    def search(self, artist_name: str) -> List[ArtistDto]:
        pass

    def get_top(self, artist_name: str) -> List[TrackDto]:
        pass

    def get_albums(self, artist_name: str) -> List[AlbumDto]:
        pass

    def get_link(self, artist_name: str) -> str:
        pass

    def get_link_on_img(self, artist_name: str) -> str:
        pass


class AbstractAlbums:
    def get(self, artist_name: str, album_name: str) -> AlbumDto:
        try:
            return self.search(artist_name, album_name)[0]
        except IndexError:
            raise NotFoundAlbumException

    def search(self, artist_name: str, album_name: str) -> List[AlbumDto]:
        pass

    def get_tracks(self, artist_name: str, album_name: str) -> List[TrackDto]:
        pass

    def get_link(self, artist_name, album_name: str) -> str:
        pass

    def get_link_on_img(self, artist_name: str, album_name: str) -> str:
        pass


class AbstractTracks:
    def get(
            self,
            artist_name: str,
            album_name: str,
            track_name: str
    ) -> TrackDto:
        try:
            return self.search(artist_name, album_name, track_name)[0]
        except IndexError:
            raise NotFoundTrackException

    def search(
            self,
            artist_name: str,
            album_name: str,
            track_name: str
    ) -> List[TrackDto]:
        pass

    def get_link(self,
                 artist_name: str,
                 album_name: str,
                 track_name: str) -> str:
        pass

    def get_link_on_img(self,
                        artist_name: str,
                        album_name: str,
                        track_name: str) -> str:
        pass


class AbstractMusicManager:
    artists: AbstractArtists
    albums: AbstractAlbums
    tracks: AbstractTracks
