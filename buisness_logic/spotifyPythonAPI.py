from buisness_logic.SpotifyWebAPI.features import Spotify
from buisness_logic.SpotifyWebAPI.core.exceptions import NotResultSearchException

_spotify = Spotify()


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
        {
            "release_date": track['album']["release_date"],
            "name": track['name'],
            "album_name": track['album']['name'],
            "top_number": index + 1,
            "disc_number": track['track_number'],
            "artist_name": track['artists'][0]['name']
        } for index, track in enumerate(tracks)
    ]
