from typing import List

import pytest

from dto import ArtistDto
from music_manger.core.exceptions import NotFoundArtistException
from music_manger.implementations.rocknation_and_spotify.spotify import Spotify
from tests.music_manager_implentations.Spotify.test_tracks import assert_is_valid_track_collection

artist_name = "Queen"
not_valid_name = "$#@!-"

artist_params = {
    "artist_name": artist_name
}
not_valid_params = {
    "artist_name": not_valid_name
}


@pytest.fixture()
def spotify():
    return Spotify()


def assert_is_valid_artist_collection(artists: List[ArtistDto]):
    for artist in artists:
        assert_is_valid_artist(artist)


def assert_is_valid_artist(artist: ArtistDto):
    fields = {
        "name": str,
        "spotify_id": str
    }

    for field_name, field_type in fields.items():
        field = getattr(artist, field_name)

        assert isinstance(field, field_type), f"Artist must have field {field_name}"


def test_get(spotify: Spotify):
    artist = spotify.artists.get(**artist_params)

    assert_is_valid_artist(artist)


def test_get_raise_not_found_artist(spotify: Spotify):
    with pytest.raises(NotFoundArtistException):
        artist = spotify.artists.get(**not_valid_params)


def test_search(spotify: Spotify):
    artists = spotify.artists.search(**artist_params)

    assert_is_valid_artist_collection(artists)


def test_search_limit(spotify: Spotify):
    artists = spotify.artists.search(**artist_params, limit=4)

    assert len(artists) == 4
    assert_is_valid_artist_collection(artists)


def test_get_top(spotify: Spotify):
    top = spotify.artists.get_top(**artist_params)

    assert len(top) == 10
    assert_is_valid_track_collection(top)
