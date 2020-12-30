from entities import Artist, Album, Track
from server import fields
from server.serializer import Serializer, GeneralSerializer


def serializing_top(top: list):
    serialized_top = []
    track_fields = ("name", "album")

    for track in top:
        track_data = EntitiesGeneralSerializer(track).get_data(*track_fields)
        serialized_top.append(track_data)

    return top


def serializing_artist(artist: Artist):
    artist_fields = ('name',)

    return EntitiesGeneralSerializer(artist).get_data(*artist_fields)


def serializing_album(album: Album):
    album_fields = ('name', 'link', 'link_on_img', 'release_date')

    return EntitiesGeneralSerializer(album).get_data(*album_fields)


def serializing_tracks(tracks: list):
    serialized_tracks = []
    track_fields = ('name', 'artist')

    for track in tracks:
        tracks_data = EntitiesGeneralSerializer(track).get_data(*track_fields)
        serialized_tracks.append(tracks_data)

    return serialized_tracks


class ArtistSerializer(Serializer):
    obj_type = Artist
    all_fields = ('name', 'top', 'link', 'link_on_img',)

    name = fields.StringField("name")
    link = fields.StringField("link")
    link_on_img = fields.StringField("link_on_img")
    top = fields.CustomField("top", serializing_top)


class AlbumSerializer(Serializer):
    obj_type = Album
    all_fields = ['name', 'tracks', 'release_date', 'artist', 'link_on_img', 'link']

    name = fields.StringField("name")
    release_date = fields.StringField("release_date")
    link = fields.StringField("link")
    link_on_img = fields.StringField("link_on_img")
    artist = fields.CustomField("artist", serializing_artist)
    tracks = fields.CustomField("tracks", serializing_tracks)


class TrackSerializer(Serializer):
    obj_type = Track
    all_fields = ('name', 'artist', 'album',)

    name = fields.StringField('name')
    artist = fields.CustomField('artist', serializing_artist)
    album = fields.CustomField('album', serializing_album)


class EntitiesGeneralSerializer(GeneralSerializer):
    all_serializers = [
        ArtistSerializer, AlbumSerializer, TrackSerializer
    ]
