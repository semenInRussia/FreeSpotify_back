"""
This package has functions for deserializing from JSON (From spotify API),
To DTO objects (ArtistDto, AlbumDto, TrackDto).
"""


from dto import AlbumDto
from dto import ArtistDto
from dto import TrackDto

from music_manger.implementations.rocknation_and_spotify.utils import delete_sound_quality


def deserialize_artists(json_response: list) -> list:
    return [
        ArtistDto(
            name=delete_sound_quality(artist_data['name']),
            spotify_id=artist_data['id']
        ) for artist_data in json_response
    ]


def deserialize_artists_when_search(json_response: dict) -> list:
    return deserialize_artists(json_response['artists']['items'])


def deserialize_albums(json_response: dict) -> list:
    return [
        AlbumDto(
            name=delete_sound_quality(album["name"]),
            artist_name=delete_sound_quality(album['artists'][0]['name']),
            release_date=album['release_date'],
            spotify_id=album['id']
        ) for album in json_response
    ]


def deserialize_albums_by_spotify_id(json_response: dict) -> list:
    return deserialize_albums(json_response["albums"])


def deserialize_albums_when_search(json_response: dict) -> list:
    return deserialize_albums(json_response['albums']['items'])


def deserialize_tracks(json_response: dict) -> list:
    return [
        TrackDto(
            name=delete_sound_quality(track['name']),
            album_name=delete_sound_quality(track['album']['name']),
            disc_number=track['track_number'],
            artist_name=delete_sound_quality(track['artists'][0]['name'])
        ) for track in json_response
    ]


def deserialize_tracks_when_search(json_response: dict) -> list:
    return deserialize_tracks(
        json_response['tracks']['items']
    )


def deserialize_tracks_of_album(json_response: dict, album_name: str):
    items = json_response['items']

    return [
        TrackDto(
            name=delete_sound_quality(track['name']),
            album_name=album_name,
            disc_number=track['track_number'],
            artist_name=track['artists'][0]['name']
        ) for track in items
    ]


def deserialize_tracks_of_artist_top(json_response: dict) -> list:
    return deserialize_tracks(
        json_response['tracks']
    )
