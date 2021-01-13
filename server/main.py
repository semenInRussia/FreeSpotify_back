from flask_cors import CORS, cross_origin
from flask import Flask

from entities import Track, Artist, Album
from server.serializers.entities_serializers import EntitiesSerializer
from server.urls import MAIN_PAGE_URL, ARTISTS_URL, ARTIST_DETAIL_URL, ALBUMS_URL, ALBUM_DETAIL_URL
from server.urls import TRACKS_URL, TRACK_DETAIL_URL

app = Flask(__name__)

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route(MAIN_PAGE_URL)
@cross_origin()
def main_handle():
    return {
        'Main page': MAIN_PAGE_URL,
        'Artists': ARTISTS_URL,
        'Albums': ALBUMS_URL,
        'Tracks': TRACKS_URL
    }


@app.route(ARTISTS_URL)
@cross_origin()
def artists_handle():
    return {
        'Watch detail info': ARTIST_DETAIL_URL
    }


@app.route(ARTIST_DETAIL_URL)
@cross_origin()
def artist_detail_handle(artist_name):
    artist = Artist(artist_name)
    serializer = EntitiesSerializer(artist)

    return serializer.get_data()


@app.route(ARTISTS_URL)
@cross_origin()
def albums_handle():
    return {
        'Detail': ALBUM_DETAIL_URL
    }


@app.route(ALBUM_DETAIL_URL)
@cross_origin()
def album_detail_handle(artist_name: str, name: str):
    album = Album(artist_name, name)
    serializer = EntitiesSerializer(album)

    return serializer.get_data()


@app.route(TRACKS_URL)
@cross_origin()
def tracks_handle():
    return {
        'Watch All Info': TRACK_DETAIL_URL
    }


@app.route(TRACK_DETAIL_URL)
@cross_origin()
def track_detail_handle(artist_name, album_name, name):
    track = Track(artist_name, album_name, name)
    serializer = EntitiesSerializer(track)

    return serializer.get_data()
