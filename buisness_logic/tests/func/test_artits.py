from buisness_logic.Artist import Artist

artist_name = "Metallica"


def test_init():
    Artist(artist_name)

def test_get_album_name():
    artist = Artist(artist_name)

    assert artist.name == artist_name
