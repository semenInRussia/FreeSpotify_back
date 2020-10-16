import json

import requests

view_top_url = "http://127.0.0.1:8000/api/tracks/top/{}"
not_valid_artist_name = "assss"


def test_process_exception():
    request = requests.get(
        view_top_url.format(not_valid_artist_name)
    )

    request_json = json.loads(request.text)

    assert request_json == {
        "error_description": "Artist don't find.",
        "error_name": "NotFoundArtistException"
    }
