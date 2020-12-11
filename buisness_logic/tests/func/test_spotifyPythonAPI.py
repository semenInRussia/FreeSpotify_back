import pytest

from buisness_logic.spotify.spotifyPythonAPI import Spotify

spotify = Spotify()


artist_name = 'AC/DC'
album_name = 'back in black'
track_name = 'back in black'
release_year = '1980'


def testGetTop():
    top = spotify.artists.get_top(artist_name)

    _assert_is_track_top(top)

def test_get_tracks_info():
    data = spotify.tracks.get("Ac dc - T.N.T")

    first_artist = data[0]

    assert first_artist.name == artist_name


def _assert_is_track_top(top: list) -> None:
    assert top is not None
    assert isinstance(top, list)
    assert len(top) == 10

    assert top[0].artist.name
    assert top[0].name
    assert top[0].album.name
    assert top[0].disc_number
    assert top[0].release_date

def test_search_albums():
    albums = spotify.album.search(artist_name, spotify=spotify)
    album = albums[-1]

    assert isinstance(albums, list), "search_albums() must return type - list"
    assert album.name
    assert album.artist.name
