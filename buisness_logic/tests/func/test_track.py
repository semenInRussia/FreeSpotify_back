from buisness_logic.Album import Album
from buisness_logic.Artist import Artist
from buisness_logic.Track import Track


artist_name = "Metallica"
album_name = "Master of puppets"
track_name = "Master of puppets"

def test_base_init():
    Track(artist_name, track_name, album_name)

def test_init():
    Track(artist_name, track_name, album_name, top_number=1, disc_number=2)
