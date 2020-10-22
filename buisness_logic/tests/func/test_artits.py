from buisness_logic.entities.artist import Artist
from buisness_logic.tests.func.test_spotifyPythonAPI import _assert_is_track_top

artist_name = "Metallica"
approximate_artist_name = "metalica"


def test_base_init():
    # Not raise exception
    Artist(artist_name=artist_name)

def test_get_album_name():
    artist = Artist(artist_name=artist_name)

    assert artist.name == artist_name

def test_get_precise_album_name():
    artist = Artist(artist_name=approximate_artist_name)

    assert artist.name == artist_name

def test_get_top():
    artist = Artist(artist_name=artist_name)

    top = artist.get_top()

    _assert_is_track_top(top)
