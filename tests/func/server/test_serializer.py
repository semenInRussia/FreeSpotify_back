from entities import Artist, Album, Track
from server.entities_serializers import ArtistSerializer, EntitiesGeneralSerializer

artist_name = "Deep Purple"
album_name = "Burn"
track_name = "Burn"


def test_artist_serializer():
    artist = Artist(artist_name)

    data = ArtistSerializer(artist).get_data("name", "top")

    fields = ["name", "top"]

    for field in fields:
        assert field in data


def test_general_serializer_artist():
    artist = Artist(artist_name)

    data = EntitiesGeneralSerializer(artist).get_data("name", "top")

    fields = ["name", "top"]

    for field in fields:
        assert field in data


def test_general_serializer_album():
    album = Album(artist_name, album_name)

    fields = ["name", "release_date"]

    data = EntitiesGeneralSerializer(album).get_data(*fields)

    for field in fields:
        assert field in data


def test_general_serializer_track():
    track = Track(artist_name, album_name, track_name)

    fields = ["name", "album", "artist"]

    data = EntitiesGeneralSerializer(track).get_data(*fields)

    for field in fields:
        assert field in data
