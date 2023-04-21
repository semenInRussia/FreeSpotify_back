from typing import Callable, TypeVar

from FreeSpotify_back.entities import Album, Artist, Track

from . import fields
from .serializer import GeneralSerializer, Serializer

T = TypeVar("T")
SerializeFunction = Callable[[T], dict]

def get_serialize_artist_function(*fields_to_serialize: str,
                                  ) -> SerializeFunction[Artist]:
    """Return a function that accepts an Artist and returns a dict with given fields.

    The Resulting dict is a representation of an artist
    """
    return lambda artist: ArtistSerializer(artist).get_data(*fields_to_serialize)


def get_serialize_album_function(*fields_for_serialize: str,
                                 ) -> SerializeFunction[Album]:
    """Return a function that accepts an Album and returns a dict with given fields.

    The Resulting dict is a representation of an album
    """
    return lambda album: AlbumSerializer(album).get_data(*fields_for_serialize)


def get_serialize_track_function(*fields_for_serialize: str,
                                 ) -> SerializeFunction[Track]:
    """Return a function that accepts a Track and returns a dict with given fields.

    The Resulting dict is a representation of a track
    """
    return lambda track: TrackSerializer(track).get_data(*fields_for_serialize)


class ArtistSerializer(Serializer):
    """A serializer class for Artist.

    Pass an artist to it via constructor and get dictionary using method `get_data`
    with a list of fields from which you want construct a dict
    """

    object_type = Artist

    name = fields.StringFieldSerializer()
    link = fields.StringFieldSerializer()
    link_on_img = fields.StringFieldSerializer()

    top = fields.CustomListFieldSerializer(get_serialize_track_function("name",
        "disc_number", "album", "link"))
    albums = fields.CustomListFieldSerializer(get_serialize_album_function("name",
        "link_on_img", "release_date"))


class AlbumSerializer(Serializer):
    """A serializer class for Album.

    Pass an Album to it via constructor and get dictionary using method `get_data`
    with a list of fields from which you want construct a dict
    """

    object_type = Album

    name = fields.StringFieldSerializer()
    release_date = fields.StringFieldSerializer()
    link = fields.StringFieldSerializer()
    link_on_img = fields.StringFieldSerializer()

    artist = fields.CustomFieldSerializer(
        get_serialize_artist_function("name", "link_on_img"))
    tracks = fields.CustomListFieldSerializer(
        get_serialize_track_function("name", "disc_number", "link"))


class TrackSerializer(Serializer):
    """A serializer class for Track.

    Pass a track to it via constructor and get dictionary using method `get_data`
    with a list of fields from which you want construct a dict
    """

    object_type = Track

    name = fields.StringFieldSerializer()
    disc_number = fields.IntegerFieldSerializer()

    artist = fields.CustomFieldSerializer(
        get_serialize_artist_function("name", "link_on_img"))
    album = fields.CustomFieldSerializer(
        get_serialize_album_function("name", "link_on_img", "release_date"))

    link = fields.StringFieldSerializer()


class EntitiesSerializer(GeneralSerializer):
    """A serializer class for entities of `FreeSpotify_back`: Artist, Album and Track.

    Pass an entity to it via constructor and get dictionary using method `get_data`
    with a list of fields from which you want construct a dict
    """

    all_serializers = [
        ArtistSerializer,
        AlbumSerializer,
        TrackSerializer,
    ]
