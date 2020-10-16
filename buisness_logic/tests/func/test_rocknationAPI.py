from backend.buisness_logic.rocknationAPI import get_link_on_artist, get_link_on_track, get_link_on_album, \
    get_link_on_album_img

ac_dc_spotify_id = '711MCceyCBcFnzjGY4Q7Un'

artist_name = 'AC/DC'
album_name = 'back in black'
track_name = 'back in black'
release_year = '1980'


def test_get_link_on_artist():
    link = get_link_on_artist(artist_name)

    assert link is not None
    assert link == "https://rocknation.su/mp3/band-1"


def test_get_link_on_album():
    link = get_link_on_album(artist_name, album_name, raise_exception=False)

    assert link is not None
    assert link == "https://rocknation.su/mp3/album-9"


def test_get_link_on_album_img_by():
    link = get_link_on_album_img(artist_name, album_name)

    assert link == "https://rocknation.su/upload/images/albums/9.jpg"
