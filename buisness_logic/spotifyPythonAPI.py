from typing import List

from loguru import logger

from buisness_logic.SpotifyWebAPI.core.exceptions import NotResultSearchException
from buisness_logic.SpotifyWebAPI.features import Spotify
from buisness_logic.album import Album
from buisness_logic.track import Track

_spotify = Spotify()


def _filter_albums_for_search_albums_by_spotify_id(json_response: dict):
    return _filter_albums(json_response["albums"])


def _filter_albums_for_search_albums(json_response: dict):
    return _filter_albums(json_response['albums']['items'])


def _filter_albums(albums_info: dict) -> List[Album]:
    return [
        Album(
            album_name=album["name"],
            artist_name=album['artists'][0]['name'],
            spotify_id=album['id']
        ) for album in albums_info
    ]


def search_albums(search_string: str, spotify: Spotify, limit: int = 4, offset: int = 0) -> List[Album]:
    # "album" - type searching
    # link on doc for search -
    # https://developer.spotify.com/console/get-search-item/https://developer.spotify.com/documentation/web-api/reference/search/search/
    search_data = spotify.search(q=search_string, type_="album", limit=limit, offset=offset)

    logger.info(f"search_data = {search_data}")

    return _filter_albums_for_search_albums(search_data)


def search_albums_by_spotify_id(spotify_album_ids: str, spotify: Spotify) -> List[Album]:
    logger.info(f"album_ids = {spotify_album_ids}")
    json_response = spotify.get_album_info(spotify_album_ids)
    logger.info(f"json_response = {json_response}")

    return _filter_albums_for_search_albums_by_spotify_id(json_response)


def get_track_info(artist_name: str, track_name: str, spotify: Spotify) -> dict:
    search_text = f"{artist_name} - {track_name}"

    tracks_info_at_search = get_tracks_info(search_text, spotify=spotify)

    try:
        first_track_info = tracks_info_at_search[0]
    except IndexError:
        raise NotResultSearchException

    return first_track_info


def get_artist_info(artist_name: str, spotify: Spotify) -> dict:
    artists_info = get_artists_ids_and_names(artist_name, spotify)

    return artists_info[0]


def get_disc_number(artist_name, track_name, spotify: Spotify) -> int:
    return get_track_info(artist_name, track_name, spotify=spotify).get('disc_number')


def get_track_name(artist_name: str, track_name: str):
    track_info = get_track_info(artist_name, track_name, _spotify)
    return track_info.get('name')


def get_top_music_info_by_approximate_artist_title(approximate_artist_title: str, spotify: Spotify,
                                                   country: str = 'US') -> list:
    artists = get_artists_ids_and_names(approximate_artist_title, spotify)
    first_artist = artists[0]

    first_artist_id = first_artist['artist_id']

    top = get_top_music_info(first_artist_id, spotify, country=country)

    return top


def get_artists_ids_and_names(approximate_artist_title: str, spotify: Spotify, limit: int = 1, offset: int = 0) -> list:
    full_data = spotify.search(q=approximate_artist_title, type_='artist', limit=limit, offset=offset)

    full_data_items = full_data['artists']['items']

    return _filter_artists_search_data(full_data_items)


def get_tracks_info(search_text: str, spotify: Spotify, limit: int = 1, offset: int = 0) -> list:
    full_data = spotify.search(q=search_text, type_='track', limit=limit, offset=offset)

    full_data_items = full_data['tracks']['items']

    return _filter_tracks(full_data_items)


def get_top_music_info(spotify_artist_id: str, spotify: Spotify, country: str = 'US'):
    full_data = spotify.get_top_tracks(spotify_artist_id, country=country)
    tracks = full_data['tracks']

    return _filter_tracks(tracks)


def _filter_artists_search_data(artists_data: dict) -> list:
    return [{'artist_name': artist_data['name'], 'artist_id': artist_data['id']} for artist_data in artists_data
            ]


def _filter_tracks(tracks: dict) -> list:
    return [
        Track(release_date=track['album']["release_date"],
              track_name=track['name'],
              album_name=track['album']['name'],
              top_number=index + 1,
              disc_number=track['track_number'],
              artist_name=track['artists'][0]['name'])
        for index, track in enumerate(tracks)
    ]
