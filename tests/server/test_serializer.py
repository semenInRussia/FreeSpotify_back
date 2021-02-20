from entities import Artist, Album, Track
from server.serializers.entities_serializers import EntitiesSerializer
from tests.settigs_for_test import settings_with_mock

artist_name = "Deep Purple"
album_name = "Burn"
track_name = "Burn"


def test_general_serializer_artist():
    artist = Artist(artist_name, additional_settings=settings_with_mock)

    data = EntitiesSerializer(artist).get_data("name", "top")

    fields = ["name", "top"]

    for field in fields:
        assert field in data


def test_general_serializer_album():
    album = Album(artist_name, album_name, additional_settings=settings_with_mock)

    fields = ["name", "release_date"]

    data = EntitiesSerializer(album).get_data(*fields)

    for field in fields:
        assert field in data


def test_general_serializer_track():
    track = Track(artist_name, album_name, track_name, additional_settings=settings_with_mock)

    fields = ["name", "album", "artist"]

    data = EntitiesSerializer(track).get_data(*fields)

    for field in fields:
        assert field in data
