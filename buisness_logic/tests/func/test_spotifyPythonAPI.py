from buisness_logic.dto import TrackDto
from buisness_logic.spotify.spotifyPythonAPI import Spotify

spotify = Spotify()

artist_name = 'AC/DC'
album_name = 'Back In Black'
track_name = 'Back In Black'
release_year = '1980'


def test_get_top():
    top = spotify.artists.get_top(artist_name)

    _assert_is_track_dto_top(top)


def _assert_is_track_dto_top(top: list):
    assert top is not None
    assert isinstance(top, list)
    assert len(top) == 10

    assert isinstance(top[0], TrackDto)


def test_get_track():
    track = spotify.tracks.get(artist_name, track_name)

    assert track.name == track_name


def test_search_tracks():
    tracks = spotify.tracks.search(artist_name, track_name)

    first_track = tracks[0]

    assert first_track.name == track_name


def test_search_albums():
    albums = spotify.albums.search(artist_name, album_name)
    album = albums[-1]

    assert isinstance(albums, list)
    assert album.name
    assert album.artist_name


def test_get_album():
    album = spotify.albums.get(artist_name, album_name)

    assert album.name == album_name
    assert album.artist_name == artist_name
