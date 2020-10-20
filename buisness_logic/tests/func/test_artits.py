from buisness_logic.Artist import Artist
from buisness_logic.tests.func.test_spotifyPythonAPI import _assert_is_valid_track_info

artist_name = "Metallica"
approximate_artist_name = "metalica"


def test_base_init():
    # Not raise exception
    Artist(artist_name)

def test_get_album_name():
    artist = Artist(artist_name)

    assert artist.name == artist_name

def test_get_precise_album_name():
    artist = Artist(approximate_artist_name)

    assert artist.name == artist_name

def test_get_top():
    artist = Artist(artist_name)

    top = artist.get_top()

    _assert_is_valid_track_info(top)
