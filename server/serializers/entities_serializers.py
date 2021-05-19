from entities import Album
from entities import Artist
from entities import Track

from server.serializers import fields

from server.serializers.serializer import GeneralSerializer
from server.serializers.serializer import Serializer


def get_serialize_artist_function(*fields_for_serialize):
    return lambda artist: ArtistSerializer(artist).get_data(*fields_for_serialize)


def get_serialize_album_function(*fields_for_serialize):
    return lambda album: AlbumSerializer(album).get_data(*fields_for_serialize)


def get_serialize_track_function(*fields_for_serialize):
    return lambda track: TrackSerializer(track).get_data(*fields_for_serialize)


class ArtistSerializer(Serializer):
    object_type = Artist

    name = fields.StringFieldSerializer()
    link = fields.StringFieldSerializer()
    link_on_img = fields.StringFieldSerializer()

    top = fields.CustomListFieldSerializer(get_serialize_track_function("name", "disc_number", "album"))
    albums = fields.CustomListFieldSerializer(get_serialize_album_function("name", "link_on_img"))


class AlbumSerializer(Serializer):
    object_type = Album

    name = fields.StringFieldSerializer()
    release_date = fields.StringFieldSerializer()
    link = fields.StringFieldSerializer()
    link_on_img = fields.StringFieldSerializer()

    artist = fields.CustomFieldSerializer(get_serialize_artist_function("name", "link_on_img"))
    tracks = fields.CustomListFieldSerializer(get_serialize_track_function("name", "disc_number"))


class TrackSerializer(Serializer):
    object_type = Track

    name = fields.StringFieldSerializer()
    disc_number = fields.IntegerFieldSerializer()

    artist = fields.CustomFieldSerializer(get_serialize_artist_function("name", "link_on_img"))
    album = fields.CustomFieldSerializer(get_serialize_album_function("name", "link_on_img", "release_date"))


class EntitiesSerializer(GeneralSerializer):
    all_serializers = [
        ArtistSerializer,
        AlbumSerializer,
        TrackSerializer,
    ]
