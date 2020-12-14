from dto import TrackDto
from music_manger.implementations.RocknationAndSpotify.rocknation_and_spotify import RocknationAndSpotify
from music_manger.implementations.RocknationAndSpotify.spotify import Spotify

spotify = RocknationAndSpotify()

artist_name = 'AC/DC'
album_name = 'Back In Black'
track_name = 'Back In Black'

num_tracks_in_album = 10

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


def test_delete_sound_quality_when_get_album():
    new_artist_name = 'Black Sabbath'
    new_album_name = 'Paranoid'

    album = spotify.albums.get(new_artist_name, new_album_name)

    assert album.name == new_album_name


def test_get_tracks_of_album():
    tracks = spotify.albums.get_tracks(artist_name, album_name)

    assert isinstance(tracks[0], TrackDto)
    assert isinstance(tracks, list)
    assert len(tracks) == num_tracks_in_album
