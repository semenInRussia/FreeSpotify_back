from buisness_logic.album import Album
from buisness_logic.artist import Artist
from buisness_logic.track import Track


artist_name = "Metallica"
album_name = "Master of puppets"
track_name = "Master of puppets"

def test_base_init():
    Track(artist_name, track_name, album_name)

def test_init():
    Track(artist_name, track_name, album_name, top_number=1, disc_number=2)

def test_track_artist():
    track = Track(artist_name, album_name, track_name)

    assert track.artist.name == artist_name

def test_track_album():
    track = Track(artist_name, album_name, track_name)

    assert track.album.name == album_name
