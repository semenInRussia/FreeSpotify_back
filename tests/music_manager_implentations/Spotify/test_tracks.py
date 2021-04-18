from typing import List

from dto import TrackDto
from .fixtures import *

artist_name = "Queen"
album_name = "News of the World"
track_name = "We are the CHAMPIONS"

track_params = {
    "artist_name": artist_name,
    "album_name": album_name,
    "track_name": track_name
}


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
    track = spotify.tracks.get(**track_params)

    assert_is_valid_track(track)

def test_search(spotify: Spotify):
    tracks = spotify.tracks.search(**track_params)

    assert_is_valid_track_collection(tracks)

def test_search_limit(spotify: Spotify):
    tracks = spotify.tracks.search(**track_params, limit=4)

    assert len(tracks) == 4
    assert_is_valid_track_collection(tracks)

