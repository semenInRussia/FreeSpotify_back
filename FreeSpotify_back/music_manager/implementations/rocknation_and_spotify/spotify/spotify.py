from collections.abc import Iterable
from typing import Optional

from FreeSpotify_back._low_level_utils import cached_function
from FreeSpotify_back.dto import AlbumDto, ArtistDto, TrackDto
from FreeSpotify_back.music_manager import (
    AbstractAlbums,
    AbstractArtists,
    AbstractTracks,
)

from ._deserializers import (
    deserialize_albums_from_search_response,
    deserialize_albums_of_artist_response,
    deserialize_artists_from_search_response,
    deserialize_tracks_from_artist_top_response,
    deserialize_tracks_from_search_response,
    deserialize_tracks_of_album_from_response,
)
from .spotify_core import SpotifyCore


class _BaseSpotifyObject:
    def __init__(self, spotify_core: Optional[SpotifyCore] = None):
        super().__init__()

        self._init_spotify_core(spotify_core)

    def _init_spotify_core(self, spotify_core: Optional[SpotifyCore]):
        if spotify_core:
            self._spotify_core = spotify_core
        else:
            self._spotify_core = SpotifyCore()


class SpotifyArtists(AbstractArtists, _BaseSpotifyObject):
    @cached_function
    def search(
        self, artist_name: str, limit: int = 1, offset: int = 0
    ) -> Iterable[ArtistDto]:
        json_response = self._spotify_core.parse_search_json(
            artist_name, type_="artist", limit=limit, offset=offset
        )
        return deserialize_artists_from_search_response(json_response)

    def get_top(self, artist_name: str) -> list:
        artist_id = self.get(artist_name).spotify_id
        return self._get_top_by_spotify_id(artist_id)

    @cached_function
    def _get_top_by_spotify_id(
        self, spotify_artist_id: str, market: str = "US"
    ) -> list[TrackDto]:
        json_response = self._spotify_core.parse_tracks_of_top(
            spotify_artist_id, market=market
        )
        return deserialize_tracks_from_artist_top_response(json_response)

    def get_albums(
        self, artist_name: str, limit: int = 1, offset: int = 0
    ) -> list[AlbumDto]:
        """Return a list of DTOs of albums."""
        artist_id = self.get(artist_name).spotify_id
        return self._get_albums_by_spotify_id(artist_id, limit, offset)

    @cached_function
    def _get_albums_by_spotify_id(
        self, artist_id: str, limit: int, offset: int
    ) -> list[AlbumDto]:
        json_response = self._spotify_core.parse_albums_of_artist(
            artist_id,
            limit=limit,
            offset=offset,
        )

        return deserialize_albums_of_artist_response(json_response)


class SpotifyAlbums(AbstractAlbums, _BaseSpotifyObject):
    @cached_function
    def search(
        self, artist_name: str, album_name: str, limit: int = 1, offset: int = 0
    ) -> list[AlbumDto]:
        search_string = f"{artist_name} - {album_name}"

        albums = self.query(search_string, limit=limit, offset=offset)

        return albums

    def query(
        self, search_string: str, limit: int = 1, offset: int = 0
    ) -> list[AlbumDto]:
        json_response = self._spotify_core.parse_search_json(
            q=search_string, type_="album", limit=limit, offset=offset
        )
        albums = deserialize_albums_from_search_response(json_response)
        return albums

    def get_tracks(self, artist_name: str, album_name: str):
        album_id = self.get(artist_name, album_name).spotify_id

        json_response = self._spotify_core.parse_tracks_of_album(album_id)

        tracks = deserialize_tracks_of_album_from_response(json_response, album_name)

        return tracks


class SpotifyTracks(AbstractTracks, _BaseSpotifyObject):
    @cached_function
    def search(
        self,
        artist_name: str,
        album_name: str,
        track_name: str,
        limit: int = 1,
        offset: int = 0,
    ):
        search_text = f"{artist_name} - {track_name}"

        tracks = self.query(
            search_text,
            limit=limit,
            offset=offset,
        )

        return tracks

    def query(self, search_text: str, limit: int = 1, offset: int = 0):
        json_response = self._spotify_core.parse_search_json(
            q=search_text,
            type_="track",
            limit=limit,
            offset=offset,
        )
        tracks = deserialize_tracks_from_search_response(json_response)

        return tracks


class Spotify:
    tracks = SpotifyTracks()
    albums = SpotifyAlbums()
    artists = SpotifyArtists()
