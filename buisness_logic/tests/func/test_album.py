from buisness_logic.entities.album import Album

album_name = "Paranoid"
artist_name = "Black sabbath"

approximate_album_name = "paRanid"

def test_album():
    Album(artist_name, album_name)

def test_name():
    album = Album(artist_name, album_name)

    assert album.name == album_name

def test_precise_name():
    album = Album(artist_name, approximate_album_name)

    assert album.name == album_name
