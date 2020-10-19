from buisness_logic.Album import Album
from buisness_logic.Artist import Artist
from buisness_logic.Track import Track


artist_name = "Metallica"
album_name = "Master of puppets"

def test_init():
    Track(Artist(artist_name), Album(artist_name, album_name))
