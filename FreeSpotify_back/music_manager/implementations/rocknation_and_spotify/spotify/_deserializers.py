from FreeSpotify_back.dto import AlbumDto, ArtistDto, TrackDto
from FreeSpotify_back.music_manager.utils import delete_sound_quality


def deserialize_artists_from_response(json_response: list) -> list[ArtistDto]:
    return [
        ArtistDto(
            name=delete_sound_quality(artist_data['name']),
            spotify_id=artist_data['id'],
        ) for artist_data in json_response
    ]


def deserialize_artists_from_search_response(json_response: dict) -> list[ArtistDto]:
    return deserialize_artists_from_response(json_response['artists']['items'])


def deserialize_albums_from_response(json_response: dict) -> list[AlbumDto]:
    return [
        AlbumDto(
            artist_name=delete_sound_quality(album['artists'][0]['name']),
            name=delete_sound_quality(album["name"]),
            release_date=album['release_date'],
            spotify_id=album['id'],
        ) for album in json_response
    ]


def deserialize_albums_from_search_response(json_response: dict) -> list[AlbumDto]:
    return deserialize_albums_from_response(json_response['albums']['items'])


def deserialize_albums_of_artist_response(json_response: dict) -> list[AlbumDto]:
    return deserialize_albums_from_response(json_response['items'])


def deserialize_tracks_from_response(json_response: dict) -> list[TrackDto]:
    return [
        TrackDto(
            artist_name=delete_sound_quality(track['artists'][0]['name']),
            album_name=delete_sound_quality(track['album']['name']),
            name=delete_sound_quality(track['name']),
            disc_number=track['track_number'],
        ) for track in json_response
    ]


def deserialize_tracks_from_search_response(json_response: dict) -> list[TrackDto]:
    return deserialize_tracks_from_response(json_response['tracks']['items'])


def deserialize_tracks_of_album_from_response(json_response: dict,
                                              album_name: str) -> list[TrackDto]:
    items = json_response['items']
    return [
        TrackDto(
            artist_name=delete_sound_quality(track['artists'][0]['name']),
            album_name=delete_sound_quality(album_name),
            name=delete_sound_quality(track['name']),
            disc_number=track['track_number'],
        ) for track in items
    ]


def deserialize_tracks_from_artist_top_response(json_response: dict) -> list[TrackDto]:
    return deserialize_tracks_from_response(json_response['tracks'])
