from buisness_logic.Artist import Artist

artist_name = "Metallica"
approximate_artist_name = "metalica"


def test_init():
    # Not raise exception
    Artist(artist_name)

def test_get_album_name():
    artist = Artist(artist_name)

    assert artist.name == artist_name

def test_get_precise_album_name():
    artist = Artist(approximate_artist_name)

    assert artist.name == artist_name
