from flask import Flask
from flask_cors import CORS, cross_origin

from FreeSpotify_back.entities import Album, Artist, Track

from .serializers.entities_serializers import EntitiesSerializer
from .urls import (
    ALBUM_DETAIL_PAGE_URL,
    ALBUMS_WELCOME_PAGE_URL,
    ARTIST_DETAIL_PAGE_URL,
    ARTISTS_WELCOME_PAGE_URL,
    MAIN_PAGE_URL,
    TRACK_DETAIL_PAGE_URL,
    TRACKS_WELCOME_PAGE_URL,
)

app = Flask(__name__)

cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"


@app.route(MAIN_PAGE_URL)
@cross_origin()
def main_handle() -> dict:
    """Handle function of the main server endpoint."""
    return {
        "Main page": MAIN_PAGE_URL,
        "Artists": ARTISTS_WELCOME_PAGE_URL,
        "Albums": ALBUMS_WELCOME_PAGE_URL,
        "Tracks": TRACKS_WELCOME_PAGE_URL,
    }


@app.route(ARTISTS_WELCOME_PAGE_URL)
@cross_origin()
def artists_handle() -> dict:
    """Handle function to the root URL of artists endpoints."""
    return {
        "Watch detail info": ARTIST_DETAIL_PAGE_URL,
    }


@app.route(ARTIST_DETAIL_PAGE_URL)
@cross_origin()
def artist_detail_handle(artist_name: str) -> dict:
    """Handle function to view detail information about an artist."""
    artist = Artist(artist_name)
    serializer = EntitiesSerializer(artist)

    return serializer.get_data()


@app.route(ALBUMS_WELCOME_PAGE_URL)
@cross_origin()
def albums_handle() -> dict:
    """Handle function to view information about albums endpoints."""
    return {
        "Detail": ALBUM_DETAIL_PAGE_URL,
    }


@app.route(ALBUM_DETAIL_PAGE_URL)
@cross_origin()
def album_detail_handle(artist_name: str, name: str) -> dict:
    """Handle function to view detail information about an album."""
    album = Album(artist_name, name)
    serializer = EntitiesSerializer(album)

    return serializer.get_data()


@app.route(TRACKS_WELCOME_PAGE_URL)
@cross_origin()
def tracks_handle() -> dict:
    """Handle function to view information about tracks endpoints."""
    return {
        "Watch All Info": TRACK_DETAIL_PAGE_URL,
    }


@app.route(TRACK_DETAIL_PAGE_URL)
@cross_origin()
def track_detail_handle(artist_name: str, album_name: str, name: str) -> dict:
    """Handle function to view detail information about a track."""
    track = Track(artist_name, album_name, name)
    serializer = EntitiesSerializer(track)

    return serializer.get_data()
