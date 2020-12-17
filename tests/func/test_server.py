from my_request import Requester

requester = Requester()

tracks_page = 'http://127.0.0.1:8000/api/tracks'
main_page = 'http://127.0.0.1:8000/api/'

tracks_detail_page = "http://127.0.0.1:8000/api/tracks/detail/ac-dc/back-in-black/back-in-black"

def test_main_page():
    assert_is_valid_response(main_page)


def assert_is_valid_response(url: str, method_name: str = 'get', valid_status_code: int = 200):
    json_data = requester.get_json(url, method_name)
    assert isinstance(json_data, dict)
    request = requester.create_request(url, method_name)
    assert request.status_code == valid_status_code


def test_tracks():
    assert_is_valid_response(tracks_page)

def test_track_detail():
    assert_is_valid_response(tracks_detail_page)
    tracks_data = requester.get_json(tracks_detail_page)

    assert 'name' in tracks_data
    assert 'artist' in tracks_data
    assert 'album' in tracks_data
