from dto import TrackDto, ArtistDto, AlbumDto
from music_manger.implementations.rocknation_and_spotify.utils import delete_sound_quality


def filter_artists(artists_data: list) -> list:
    return [
        ArtistDto(
            name=delete_sound_quality(artist_data['name']),
            spotify_id=artist_data['id']
        ) for artist_data in artists_data
    ]


def filter_albums(albums_info: dict) -> list:
    return [
        AlbumDto(
            name=delete_sound_quality(album["name"]),
            artist_name=delete_sound_quality(album['artists'][0]['name']),
            release_date=album['release_date'],
            spotify_id=album['id']
        ) for album in albums_info
    ]


def filter_tracks(tracks: dict) -> list:
    return [
        TrackDto(
            name=delete_sound_quality(track['name']),
            album_name=delete_sound_quality(track['album']['name']),
            disc_number=track['track_number'],
            artist_name=track['artists'][0]['name']
        ) for index, track in enumerate(tracks)
    ]


def filter_tracks_of_album(tracks: dict, album_name: str):
    items = tracks['items']

    return [
        TrackDto(
            name=delete_sound_quality(track['name']),
            album_name=album_name,
            disc_number=track['track_number'],
            artist_name=track['artists'][0]['name']
        ) for track in items
    ]


def filter_artists_search_data(json_response: dict) -> list:
    artists_data = json_response['artists']['items']

    return filter_artists(artists_data)


def filter_albums_by_spotify_id(json_response: dict) -> list:
    return filter_albums(json_response["albums"])


def filter_albums_for_searching(json_response: dict) -> list:
    return filter_albums(json_response['albums']['items'])
