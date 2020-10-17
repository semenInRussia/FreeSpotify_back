# Test views.py here...
import json

import requests

from buisness_logic.tests.func.test_spotifyPythonAPI import _assert_is_valid_track_info
from core.features.pytest import assert_is_valid_request

artist_name = 'ac dc'
album_name = 'back in black'
track_name = 'hells bells'

track_view_url = f"http://localhost:8000/api/tracks/{artist_name}/{album_name}/{track_name}"


def test_get_track_view():
    response = requests.get(track_view_url)

    assert_is_valid_request(response)

    data = json.loads(response.text)

    _assert_is_valid_track_info(data)
