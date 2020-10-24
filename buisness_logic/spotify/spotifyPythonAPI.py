from typing import List

from loguru import logger

from buisness_logic.spotify.core.exceptions import NotResultSearchException
from buisness_logic.spotify.spotifyCore import SpotifyCore


class Spotify:
    def __init__(self, spotify_core: SpotifyCore = None):
        if spotify_core is None:
            self._spotify_core = SpotifyCore()
        else:
            self._spotify_core = spotify_core

    def _filter_albums_for_search_albums_by_spotify_id(self, json_response: dict):
        return self._filter_albums(json_response["albums"])

    def _filter_albums_for_search_albums(self, json_response: dict):
        return self._filter_albums(json_response['albums']['items'])

    from buisness_logic.entities.album import Album

    @staticmethod
    def _filter_albums(albums_info: dict) -> List[Album]:
        from buisness_logic.entities.album import Album

        return [
            Album(
                album_name=album["name"],
                artist_name=album['artists'][0]['name'],
                spotify_id=album['id']
            ) for album in albums_info
        ]

    def search_albums(self, search_string: str, limit: int = 4, offset: int = 0) -> List[Album]:
        # "album" - type searching
        # link on doc for search -
        # https://developer.spotify.com/console/get-search-item/https://developer.spotify.com/documentation/web-api/reference/search/search/
        search_data = self._spotify_core.search(q=search_string, type_="album", limit=limit, offset=offset)

        logger.info(f"search_data = {search_data}")

        return self._filter_albums_for_search_albums(search_data)

    def search_albums_by_spotify_id(self, spotify_album_ids: str) -> List[Album]:
        logger.info(f"album_ids = {spotify_album_ids}")
        json_response = self._spotify_core.get_album_info(spotify_album_ids)
        logger.info(f"json_response = {json_response}")

        return self._filter_albums_for_search_albums_by_spotify_id(json_response)

    from buisness_logic.entities.track import Track

    def get_track_info(self, artist_name: str, track_name: str) -> Track:
        search_text = f"{artist_name} - {track_name}"

        tracks_info_at_search = self.get_tracks_info(search_text)

        try:
            first_track = tracks_info_at_search[0]
        except IndexError:
            raise NotResultSearchException

        return first_track

    def get_artist_info(self, artist_name: str) -> dict:
        artists_info = self.get_artists_ids_and_names(artist_name)

        return artists_info[0]

    def get_top_music_info_by_approximate_artist_title(self, approximate_artist_title: str,) -> list:
        artists = self.get_artists_ids_and_names(approximate_artist_title)
        first_artist = artists[0]

        first_artist_id = first_artist['artist_id']

        top = self.get_top_music_info(first_artist_id)

        return top

    def get_artists_ids_and_names(self, approximate_artist_title: str, limit: int = 1,
                                  offset: int = 0) -> list:
        full_data = self._spotify_core.search(q=approximate_artist_title, type_='artist', limit=limit, offset=offset)

        full_data_items = full_data['artists']['items']

        return self._filter_artists_search_data(full_data_items)

    def get_tracks_info(self, search_text: str, limit: int = 1, offset: int = 0) -> List[Track]:
        full_data = self._spotify_core.search(q=search_text, type_='track', limit=limit, offset=offset)

        full_data_items = full_data['tracks']['items']

        return self._filter_tracks(full_data_items)

    def get_top_music_info(self, spotify_artist_id: str, country: str = 'US'):
        full_data = self._spotify_core.get_top_tracks(spotify_artist_id, country=country)
        tracks = full_data['tracks']

        return self._filter_tracks(tracks)

    @staticmethod
    def _filter_artists_search_data(artists_data: dict) -> list:
        return [{'artist_name': artist_data['name'], 'artist_id': artist_data['id']} for artist_data in artists_data
                ]

    @staticmethod
    def _filter_tracks(tracks: dict) -> List[Track]:
        from buisness_logic.entities.track import Track

        return [
            Track(release_date=track['album']["release_date"],
                  track_name=track['name'],
                  album_name=track['album']['name'],
                  top_number=index + 1,
                  disc_number=track['track_number'],
                  artist_name=track['artists'][0]['name'])
            for index, track in enumerate(tracks)
        ]
