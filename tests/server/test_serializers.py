from FreeSpotify_back.entities import Album, Artist, Track
from FreeSpotify_back.server.serializers.entities_serializers import EntitiesSerializer

from tests.settigs_for_test import settings_with_mock

artist_name = "Deep Purple"
album_name = "Burn"
track_name = "Burn"


def test_general_serializer_artist():
    artist = Artist(artist_name, additional_settings=settings_with_mock)

    fields = ["name", "top", "link", "link_on_img", "albums"]

    data = EntitiesSerializer(artist).get_data(*fields)

    for field in fields:
        assert field in data


def test_general_serializer_album():
    album = Album(artist_name, album_name, additional_settings=settings_with_mock)

    fields = ["name", "release_date", "artist", "link", "link_on_img"]

    data = EntitiesSerializer(album).get_data(*fields)

    for field in fields:
        assert field in data


def test_general_serializer_track():
    track = Track(
        artist_name, album_name, track_name, additional_settings=settings_with_mock
    )

    fields = ["name", "album", "artist", "disc_number"]

    data = EntitiesSerializer(track).get_data(*fields)

    for field in fields:
        assert field in data
