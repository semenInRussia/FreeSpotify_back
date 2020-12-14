from typing import List

from loguru import logger

from core.exceptions import NotFoundAlbumException, NotFoundArtistException
from dto import AlbumDto, ArtistDto

from .core.exceptions import NotResultSearchException
from .spotifyCore import SpotifyCore
from ._filtres import filter_artists_search_data, filter_tracks, filter_albums_for_searching, filter_tracks_of_album


class _BaseSpotifyObject:
    def __init__(self, spotify_core: SpotifyCore = None):
        super().__init__()

        self._init_spotify_core(spotify_core)

    def _init_spotify_core(self, spotify_core):
        if spotify_core is None:
            self._spotify_core = SpotifyCore()
        else:
            self._spotify_core = spotify_core


class SpotifyArtists(_BaseSpotifyObject):
    def get(self, artist_name: str) -> ArtistDto:
        try:
            return self.search(artist_name)[0]
        except IndexError:
            raise NotFoundArtistException

    def search(self, artist_name: str, limit: int = 1, offset: int = 0) -> List[ArtistDto]:
        data = self._spotify_core.search(artist_name,
                                         type_="artist",
                                         limit=limit,
                                         offset=offset)

        return filter_artists_search_data(data)

    def get_top(self, artist_name: str, ) -> list:
        artist = self.get(artist_name)

        top = self._get_top_by_spotify_id(artist.spotify_id)

        return top

    def _get_top_by_spotify_id(self, spotify_artist_id: str, country: str = 'US'):
        full_data = self._spotify_core.get_top_tracks(spotify_artist_id, country=country)
        tracks = full_data['tracks']

        return filter_tracks(tracks)


class SpotifyAlbums(_BaseSpotifyObject):
    def search(self, artist_name: str, album_name: str, limit: int = 1, offset: int = 0) -> List[AlbumDto]:
        # "album" - type searching
        # link on doc for search -
        # https://developer.spotify.com/console/get-search-item/https://developer.spotify.com/documentation/web-api/reference/search/search/

        search_string = f"{artist_name} - {album_name}"

        albums = self._search_by_text(search_string,
                                      limit=limit,
                                      offset=offset)

        return albums

    def _search_by_text(self, search_string: str, limit: int = 1, offset: int = 0) -> List[AlbumDto]:
        searching_data = self._spotify_core.search(q=search_string, type_="album", limit=limit, offset=offset)

        logger.info(f"search_data = {searching_data}")

        albums = filter_albums_for_searching(searching_data)

        return albums

    def get(self, artist_name: str, album_name: str) -> AlbumDto:
        albums = self.search(artist_name, album_name)

        try:
            return albums[0]
        except IndexError:
            raise NotFoundAlbumException

    def get_tracks(self, artist_name: str, album_name: str):
        album_id = self.get(artist_name, album_name).spotify_id

        not_filtered_tracks = self._spotify_core.get_tracks_of_album(album_id)

        tracks = filter_tracks_of_album(not_filtered_tracks, album_name)

        return tracks


class SpotifyTracks(_BaseSpotifyObject):

    def search(self, artist_name: str, track_name: str, limit: int = 1, offset: int = 0):
        search_text = f"{artist_name} - {track_name}"

        track = self._search_by_text(search_text,
                                     limit=limit,
                                     offset=offset)

        return track

    def _search_by_text(self, search_text: str, limit: int = 1, offset: int = 0):
        full_data = self._spotify_core.search(q=search_text, type_='track', limit=limit, offset=offset)

        full_data_items = full_data['tracks']['items']

        return filter_tracks(full_data_items)

    def get(self, artist_name: str, track_name: str):
        tracks = self.search(artist_name, track_name)

        try:
            first_track = tracks[0]
        except IndexError:
            raise NotResultSearchException

        return first_track


class Spotify:
    tracks = SpotifyTracks()
    albums = SpotifyAlbums()
    artists = SpotifyArtists()
