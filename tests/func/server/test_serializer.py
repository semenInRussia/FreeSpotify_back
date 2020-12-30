from entities import Artist
from server.entities_serializers import ArtistSerializer

artist_name = "Deep purple"


def test_artist_serializer():
    artist = Artist(artist_name)

    data = ArtistSerializer(artist).get_data("name", "top")

    fields = ["name", "top"]

    for field in fields:
        assert field in data
