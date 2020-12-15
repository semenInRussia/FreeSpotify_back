from music_manger.implementations.RocknationAndSpotify.rocknation.rocknationAPI import Rocknation
from music_manger.implementations.RocknationAndSpotify.rocknation_and_spotify import RocknationAndSpotify
from settings.general import music_manager_impl

rocknation = music_manager_impl()

artist_name = 'AC/DC'
album_name = 'Back In Black'

def test_get_link_on_album_img():
    album_img = rocknation.albums.get_link_on_img(artist_name, album_name)

    assert album_img == 'https://rocknation.su/upload/images/albums/9.jpg'

def test_get_link_on_album():
    link_on_album = rocknation.albums.get_link(artist_name, album_name)

    assert link_on_album == 'https://rocknation.su/mp3/album-9'

def test_get_link_on_artist_img():
    artist_img = rocknation.artists.get_link_on_img(artist_name)

    assert artist_img == 'https://rocknation.su/upload/images/bands/1.jpg'

def test_get_link_on_artist():
    link = rocknation.artists.get_link(artist_name)

    assert link == 'https://rocknation.su/mp3/band-1'
