from typing import List

from dto import AlbumDto, ArtistDto
from music_manger.music_manger import AbstractAlbums
from music_manger.music_manger import AbstractArtists
from music_manger.music_manger import AbstractTracks

from ._deserializers import deserialize_albums_from_search_response, deserialize_artists_from_response, \
    deserialize_artists_from_search_response
from ._deserializers import deserialize_tracks_of_album_from_response
from ._deserializers import deserialize_tracks_from_artist_top_response
from ._deserializers import deserialize_tracks_from_search_response
from .spotify_core import SpotifyCore


class _BaseSpotifyObject:
    def __init__(self, spotify_core: SpotifyCore = None):
        super().__init__()

        self._init_spotify_core(spotify_core)

    def _init_spotify_core(self, spotify_core):
        if spotify_core:
            self._spotify_core = spotify_core
        else:
            self._spotify_core = SpotifyCore()


class SpotifyArtists(AbstractArtists, _BaseSpotifyObject):
    def search(self, artist_name: str, limit: int = 1, offset: int = 0) -> List[ArtistDto]:
        json_response = self._spotify_core.parse_search_json(artist_name, type_="artist", limit=limit, offset=offset)

        return deserialize_artists_from_search_response(json_response)

    def get_top(self, artist_name: str) -> list:
        artist_id = self.get(artist_name).spotify_id

        top = self._get_top_by_spotify_id(artist_id)

        return top

    def _get_top_by_spotify_id(self, spotify_artist_id: str, market: str = 'US'):
        json_response = self._spotify_core.parse_tracks_of_top(spotify_artist_id, market=market)

        top = deserialize_tracks_from_artist_top_response(json_response)

        return top


class SpotifyAlbums(AbstractAlbums, _BaseSpotifyObject):
    def search(self, artist_name: str, album_name: str, limit: int = 1, offset: int = 0) -> List[AlbumDto]:
        search_string = f"{artist_name} - {album_name}"

        albums = self._search_by_text(
            search_string,

            limit=limit,
            offset=offset
        )

        return albums

    def _search_by_text(self, search_string: str, limit: int = 1, offset: int = 0) -> List[AlbumDto]:
        json_response = self._spotify_core.parse_search_json(q=search_string, type_="album", limit=limit, offset=offset)

        albums = deserialize_albums_from_search_response(json_response)

        return albums

    def get_tracks(self, artist_name: str, album_name: str):
        album_id = self.get(artist_name, album_name).spotify_id

        json_response = self._spotify_core.parse_tracks_of_album(album_id)

        tracks = deserialize_tracks_of_album_from_response(json_response, album_name)

        return tracks


class SpotifyTracks(AbstractTracks, _BaseSpotifyObject):
    def search(self, artist_name: str, album_name: str, track_name: str, limit: int = 1, offset: int = 0):
        search_text = f"{artist_name} - {track_name}"

        tracks = self._search_by_text(
            search_text,
            limit=limit,
            offset=offset
        )

        return tracks

    def _search_by_text(self, search_text: str, limit: int = 1, offset: int = 0):
        json_response = self._spotify_core.parse_search_json(
            q=search_text,
            type_='track',
            limit=limit,
            offset=offset
        )

        tracks = deserialize_tracks_from_search_response(json_response)

        return tracks


class Spotify:
    tracks = SpotifyTracks()
    albums = SpotifyAlbums()
    artists = SpotifyArtists()
