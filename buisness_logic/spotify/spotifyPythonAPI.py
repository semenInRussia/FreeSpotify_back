from typing import List

from loguru import logger

from buisness_logic.core.exceptions import NotFoundAlbumException, NotFoundArtistException
from buisness_logic.dto import TrackDto, AlbumDto, ArtistDto
from buisness_logic.spotify.core.exceptions import NotResultSearchException
from buisness_logic.spotify.spotifyCore import SpotifyCore


class _BaseSpotifyObject:
    def __init__(self, spotify_core: SpotifyCore = None):
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

        return self._filter_artists_search_data(data)

    def get_top(self, artist_name: str, ) -> list:
        artist = self.get(artist_name)

        top = self._get_top_by_spotify_id(artist.spotify_id)

        return top

    def _get_top_by_spotify_id(self, spotify_artist_id: str, country: str = 'US'):
        full_data = self._spotify_core.get_top_tracks(spotify_artist_id, country=country)
        tracks = full_data['tracks']

        return self._filter_tracks(tracks)

    @staticmethod
    def _filter_tracks(tracks: dict) -> list:
        return [
            TrackDto(release_date=track['album']["release_date"],
                     name=track['name'],
                     album_name=track['album']['name'],
                     top_number=index + 1,
                     disc_number=track['track_number'],
                     artist_name=track['artists'][0]['name']
                     ) for index, track in enumerate(tracks)
        ]

    @staticmethod
    def _filter_artists_search_data(json_response: dict) -> list:
        artists_data = json_response['artists']['items']

        return [
            ArtistDto(
                name=artist_data['name'],
                spotify_id=artist_data['id']
            ) for artist_data in artists_data
        ]


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

        albums = self._filter_albums_for_searching(searching_data)

        return albums

    def _filter_albums_by_spotify_id(self, json_response: dict):
        return self._filter_albums(json_response["albums"])

    def _filter_albums_for_searching(self, json_response: dict):
        return self._filter_albums(json_response['albums']['items'])

    def _filter_albums(self, albums_info: dict) -> List:
        return [
            AlbumDto(
                name=self._delete_sound_quality(album["name"]),
                artist_name=album['artists'][0]['name'],
                release_date=album['release_date']
            ) for album in albums_info
        ]

    def get(self, artist_name: str, album_name: str):
        albums = self.search(artist_name, album_name)

        try:
            return albums[0]
        except IndexError:
            raise NotFoundAlbumException

    def _delete_sound_quality(self, album_name: str):
        branch_index = album_name.find("(")
        space_before_branch = branch_index - 1

        new_string = album_name[:space_before_branch]

        return new_string


class SpotifyTracks(_BaseSpotifyObject):
    @staticmethod
    def _filter_tracks(tracks: dict) -> list:

        return [
            TrackDto(release_date=track['album']["release_date"],
                     name=track['name'],
                     album_name=track['album']['name'],
                     top_number=index + 1,
                     disc_number=track['track_number'],
                     artist_name=track['artists'][0]['name'])
            for index, track in enumerate(tracks)
        ]

    def search(self, artist_name: str, track_name: str, limit: int = 1, offset: int = 0):
        search_text = f"{artist_name} - {track_name}"

        track = self._search_by_text(search_text,
                                     limit=limit,
                                     offset=offset)

        return track

    def _search_by_text(self, search_text: str, limit: int = 1, offset: int = 0):
        full_data = self._spotify_core.search(q=search_text, type_='track', limit=limit, offset=offset)

        full_data_items = full_data['tracks']['items']

        return self._filter_tracks(full_data_items)

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
