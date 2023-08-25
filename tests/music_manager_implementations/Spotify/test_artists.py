from typing import List

import pytest
from FreeSpotify_back.dto import AlbumDto, ArtistDto
from FreeSpotify_back.music_manager.core.exceptions import NotFoundArtistError
from FreeSpotify_back.music_manager.implementations import Spotify

from .test_tracks import assert_is_valid_track_collection

artist_name = "Queen"
not_valid_name = "$#@!-"

artist_params = {"artist_name": artist_name}
not_valid_params = {"artist_name": not_valid_name}


@pytest.fixture()
def spotify():
    return Spotify()


def assert_is_valid_artist_collection(artists: List[ArtistDto]):
    for artist in artists:
        assert_is_valid_artist(artist)


def assert_is_valid_artist(artist: ArtistDto):
    fields = {"name": str, "spotify_id": str}

    for field_name, field_type in fields.items():
        field = getattr(artist, field_name)

        assert isinstance(field, field_type), f"Artist must have field {field_name}"


def test_get(spotify: Spotify):
    artist = spotify.artists.get(**artist_params)

    assert_is_valid_artist(artist)


def test_get_raise_not_found_artist(spotify: Spotify):
    with pytest.raises(NotFoundArtistError):
        artist = spotify.artists.get(**not_valid_params)


def test_search(spotify: Spotify):
    artists = spotify.artists.search(**artist_params)

    assert_is_valid_artist_collection(artists)


def test_search_limit(spotify: Spotify):
    artists = spotify.artists.search(limit=4, **artist_params)

    assert_is_valid_artist_collection(artists)
    assert len(artists) == 4


def test_get_top(spotify: Spotify):
    top = spotify.artists.get_top(**artist_params)

    assert len(top) == 10
    assert_is_valid_track_collection(top)


def test_get_albums(spotify: Spotify):
    actual = spotify.artists.get_albums(**artist_params)
    first_album = actual[0]

    assert isinstance(actual, list)
    assert actual

    assert isinstance(first_album, AlbumDto)
