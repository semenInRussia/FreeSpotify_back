from flask import Flask
from flask_cors import CORS
from flask_cors import cross_origin

from .urls import ALBUMS_WELCOME_PAGE_URL
from .urls import ALBUM_DETAIL_PAGE_URL
from .urls import ARTISTS_WELCOME_PAGE_URL
from .urls import ARTIST_DETAIL_PAGE_URL
from .urls import MAIN_PAGE_URL
from .urls import TRACKS_WELCOME_PAGE_URL
from .urls import TRACK_DETAIL_PAGE_URL

from .serializers.entities_serializers import EntitiesSerializer

from ..entities import Album
from ..entities import Artist
from ..entities import Track

app = Flask(__name__)

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route(MAIN_PAGE_URL)
@cross_origin()
def main_handle():
    return {
        'Main page': MAIN_PAGE_URL,
        'Artists': ARTISTS_WELCOME_PAGE_URL,
        'Albums': ALBUMS_WELCOME_PAGE_URL,
        'Tracks': TRACKS_WELCOME_PAGE_URL
    }


@app.route(ARTISTS_WELCOME_PAGE_URL)
@cross_origin()
def artists_handle():
    return {
        'Watch detail info': ARTIST_DETAIL_PAGE_URL
    }


@app.route(ARTIST_DETAIL_PAGE_URL)
@cross_origin()
def artist_detail_handle(artist_name):
    artist = Artist(artist_name)
    serializer = EntitiesSerializer(artist)

    return serializer.get_data()


@app.route(ALBUMS_WELCOME_PAGE_URL)
@cross_origin()
def albums_handle():
    return {
        'Detail': ALBUM_DETAIL_PAGE_URL
    }


@app.route(ALBUM_DETAIL_PAGE_URL)
@cross_origin()
def album_detail_handle(artist_name: str, name: str):
    album = Album(artist_name, name)
    serializer = EntitiesSerializer(album)

    return serializer.get_data()


@app.route(TRACKS_WELCOME_PAGE_URL)
@cross_origin()
def tracks_handle():
    return {
        'Watch All Info': TRACK_DETAIL_PAGE_URL
    }


@app.route(TRACK_DETAIL_PAGE_URL)
@cross_origin()
def track_detail_handle(artist_name, album_name, name):
    track = Track(artist_name, album_name, name)
    serializer = EntitiesSerializer(track)

    return serializer.get_data()
