from buisness_logic.entities.album import Album

album_name = "Paranoid"
artist_name = "Black sabbath"

release_date = "1970-09-18"

approximate_album_name = "paranoid  "

def test_album():
    Album(artist_name, album_name)

def test_name():
    album = Album(album_name, artist_name)

    assert album.name == album_name

def test_precise_name():
    album = Album(approximate_album_name, artist_name)

    assert album.name == album_name

def test_release_year():
    album = Album(album_name, artist_name)

    assert album.release_date == release_date
