"""
This package has functions for deserializing JSON response from spotify API,
To DTO objects (ArtistDto, AlbumDto, TrackDto).
"""


from dto import AlbumDto
from dto import ArtistDto
from dto import TrackDto

from brackets_lib import delete_all_values_with_all_brackets
from music_manger.utils import delete_sound_quality


def deserialize_artists_from_response(json_response: list) -> list:
    return [
        ArtistDto(
            name=delete_all_values_with_all_brackets(artist_data['name']),
            spotify_id=artist_data['id']
        ) for artist_data in json_response
    ]


def deserialize_artists_from_search_response(json_response: dict) -> list:
    return deserialize_artists_from_response(json_response['artists']['items'])


def deserialize_albums_from_response(json_response: dict) -> list:
    return [
        AlbumDto(
            name=delete_sound_quality(album["name"]),
            artist_name=delete_sound_quality(album['artists'][0]['name']),
            release_date=album['release_date'],
            spotify_id=album['id']
        ) for album in json_response
    ]


def deserialize_albums_from_search_response(json_response: dict) -> list:
    return deserialize_albums_from_response(json_response['albums']['items'])

def deserialize_albums_of_artist_response(json_response: dict) -> list:
    return deserialize_albums_from_response(json_response['items'])


def deserialize_tracks_from_response(json_response: dict) -> list:
    return [
        TrackDto(
            name=delete_all_values_with_all_brackets(track['name']),
            album_name=delete_all_values_with_all_brackets(track['album']['name']),
            disc_number=track['track_number'],
            artist_name=delete_all_values_with_all_brackets(track['artists'][0]['name'])
        ) for track in json_response
    ]


def deserialize_tracks_from_search_response(json_response: dict) -> list:
    return deserialize_tracks_from_response(json_response['tracks']['items'])


def deserialize_tracks_of_album_from_response(json_response: dict, album_name: str):
    items = json_response['items']

    return [
        TrackDto(
            name=delete_all_values_with_all_brackets(track['name']),
            album_name=album_name,
            disc_number=track['track_number'],
            artist_name=track['artists'][0]['name']
        ) for track in items
    ]


def deserialize_tracks_from_artist_top_response(json_response: dict) -> list:
    return deserialize_tracks_from_response(json_response['tracks'])
