from flask import Flask

from entities import Track
from server.urls import MAIN_PAGE_URL, ARTISTS_URL
from server.urls import TRACKS_URL, TRACK_DETAIL_URL

app = Flask(__name__)


@app.route(MAIN_PAGE_URL)
def main():
    return {
        'Main page': MAIN_PAGE_URL,
        'Tracks': TRACKS_URL
    }


@app.route(TRACKS_URL)
def tracks():
    return {
        'Watch All Info': TRACK_DETAIL_URL
    }


@app.route(TRACK_DETAIL_URL)
def track(artist_name, album_name, name):
    return Track(artist_name, album_name, name).data.get_serialized_data()


@app.route(ARTISTS_URL)
def artits():
    return {
        'Watch all info': ARTIST_DETAIL_URL
    }
