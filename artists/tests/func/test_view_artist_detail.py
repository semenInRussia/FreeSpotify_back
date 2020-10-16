import json

import requests

from buisness_logic.tests.func.test_publicFeatures import _assert_is_public_track_top
from core.features.pytest import assert_is_request

test_artist_name = "AC DC"
view_artist_detail_url = f"http://127.0.0.1:8000/api/artists/{test_artist_name}"


def _assert_is_artist_detail(test_artist_detail: dict):
    assert "top" in test_artist_detail
    assert "name" in test_artist_detail
    assert "img_link" in test_artist_detail

    _assert_is_public_track_top(test_artist_detail["top"])


def test_view_artist_detail():
    request = requests.get(view_artist_detail_url)

    assert_is_request(request)

    test_artist_detail = json.loads(request.text)

    _assert_is_artist_detail(test_artist_detail)
