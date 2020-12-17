from flask import Flask

from entities import Track
from settings.server import ROOT_URL

app = Flask(__name__)

base_api_url = '/api/'
full_api_url = ROOT_URL + base_api_url

tracks_url = f'{base_api_url}tracks/'
full_tracks_url = ROOT_URL + tracks_url

track_detail_url = f'{tracks_url}detail/<album_name>/<artist_name>/<name>/'
full_track_detail_url = ROOT_URL + track_detail_url


@app.route(base_api_url)
def main():
    return {
        'Main page': full_api_url,
        'Tracks': full_tracks_url
    }

@app.route(tracks_url)
def tracks():
    return {
        'Watch All Info': f'{full_track_detail_url}'
    }

@app.route(track_detail_url)
def track(artist_name, album_name, name):
    return Track(artist_name, album_name, name).data.get_serialized_data()
