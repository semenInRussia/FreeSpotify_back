from buisness_logic.entities.artist import Artist
from buisness_logic.entities.track import Track

artist_name = "Metallica"
approximate_artist_name = "metalica"


def test_base_init():
    # Not raise exception
    Artist(artist_name=artist_name)

def test_get_artist_name():
    artist = Artist(artist_name=artist_name)

    assert artist.name == artist_name

def test_get_precise_artist_name():
    artist = Artist(artist_name=approximate_artist_name)

    assert artist.name == artist_name


def _assert_is_track_top(top):
    assert len(top) == 10

    assert isinstance(top[0], Track)


def test_get_top():
    artist = Artist(artist_name=artist_name)

    top = artist.top

    _assert_is_track_top(top)
