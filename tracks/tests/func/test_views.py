# Test views.py here...
import json

import requests

from buisness_logic.tests.func.test_spotifyPythonAPI import _assert_is_valid_track_info
from core.features.pytest import assert_is_valid_request

artist_name = 'ac dc'
album_name = 'back in black'
track_name = 'hells bells'

base_url = 'http://localhost:8000/api/tracks'

track_view_url = f"{base_url}/{artist_name}/{album_name}/{track_name}"
search_view_url = f"{base_url}/search/{artist_name} - {track_name}"

def test_search_track_view():
    response = requests.get(search_view_url)

    assert_is_valid_request(response)

    data = json.loads(response.text)

    assert "name" in data[0]
    assert "album_name" in data[0]
    assert "artist_name" in data[0]

def test_get_track_view():
    response = requests.get(track_view_url)

    assert_is_valid_request(response)

    data = json.loads(response.text)

    _assert_is_valid_track_info(data)
