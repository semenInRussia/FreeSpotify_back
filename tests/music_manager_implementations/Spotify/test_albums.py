from typing import List

from FreeSpotify_back.dto import TrackDto
from FreeSpotify_back.dto import AlbumDto

from FreeSpotify_back.music_manager.core.exceptions import \
     NotFoundAlbumException
from .fixtures import *

artist_name = "Queen"
album_name = "Jazz"

albums_params = {
    "artist_name": artist_name,
    "album_name": album_name
}

not_valid_params = {
    "artist_name": "*!@",
    "album_name": "#"
}


def assert_is_valid_album_collection(albums: List[AlbumDto]):
    for album in albums:
        assert_is_valid_album(album)


def assert_is_valid_album(album: AlbumDto):
    fields = {
        "name": str,
        "artist_name": str,
        "spotify_id": str,
        "release_date": str
    }

    for field_name, field_type in fields.items():
        field = getattr(album, field_name)

        assert isinstance(field, field_type), f"Album must have field {field_name}"


def assert_is_valid_track(track: TrackDto):
    fields = {
        "name": str,
        "artist_name": str,
        "album_name": str,

        "disc_number": int
    }

    for field_name, field_type in fields.items():
        field = getattr(track, field_name)
        assert isinstance(field, field_type), f"Track must have field {field_name}"


def assert_is_valid_track_collection(track_collection: List[TrackDto]):
    for track in track_collection:
        assert_is_valid_track(track)


def test_get(spotify: Spotify):
    album = spotify.albums.get(**albums_params)

    assert_is_valid_album(album)

    assert album.name == album_name
    assert album.artist_name == artist_name


def test_get_raise_not_found_album(spotify: Spotify):
    with pytest.raises(NotFoundAlbumException):
        album = spotify.albums.get(**not_valid_params)


def test_search(spotify: Spotify):
    albums = spotify.albums.search(**albums_params)

    assert_is_valid_album_collection(albums)

def test_query(spotify: Spotify):
    albums = spotify.albums.query("Queen - Jazz")

    assert_is_valid_album_collection(albums)


def test_search_limit(spotify: Spotify):
    albums = spotify.albums.search(limit=4, **albums_params)

    assert len(albums) == 4

    assert_is_valid_album_collection(albums)


def test_get_tracks(spotify: Spotify):
    tracks = spotify.albums.get_tracks(**albums_params)

    assert len(tracks) == 18

    assert_is_valid_track_collection(tracks)

