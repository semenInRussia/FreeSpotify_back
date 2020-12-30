from entities import Artist, Album
from server import fields
from server.serializer import Serializer


def serializing_top(top: list):
    serialized_top = []

    for track in top:
        track_data = ("name", "link", "album")
        serialized_top.append(track_data)

    return top


class ArtistSerializer(Serializer):
    all_fields = ('name', 'top', 'link', 'link_on_img',)

    name = fields.StringField("name")
    link = fields.StringField("link")
    link_on_img = fields.StringField("link_on_img")
    top = fields.CustomField("top", serializing_top)


def serializing_album(album: Album):
    # todo real release
    # 'name', 'link', 'link_on_img', 'release_date'
    pass


def serializing_artist(artist: Artist):
    # todo real release
    pass


def serializing_tracks(artist: Artist):
    # todo real release
    # 'name'
    pass


class TrackSerializer(Serializer):
    all_fields = ('name', 'artist', 'album',)

    name = fields.StringField('name')
    artist = fields.CustomField('artist', serializing_artist)
    album = fields.CustomField('album', serializing_album)


class AlbumSerializer(Serializer):
    all_fields = ['name', 'tracks', 'release_date', 'artist', 'link_on_img', 'link']

    name = fields.StringField("name")
    release_data = fields.StringField("release_data")
    link = fields.StringField("link")
    link_on_img = fields.StringField("link_on_img")
    artist = fields.CustomField("artist", serializing_artist)
    tracks = fields.CustomField("tracks", serializing_tracks)


ALL_OBJECT_SERIALIZERS = [
    ArtistSerializer, AlbumSerializer, TrackSerializer
]
