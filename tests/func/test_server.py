from my_request import Requester
from server.wsgi_server import get_and_start_from_cmd

requester = Requester()

BASE_URL = 'http://127.0.0.1:5353'

tracks_page = f"{BASE_URL}/api/tracks"
main_page = f"{BASE_URL}/api/"

tracks_detail_page = "{BASE_URL}/api/tracks/detail/ac-dc/back-in-black/back-in-black"


def server(func):
    def new_func(*args, **kwargs):
        server_ = get_and_start_from_cmd(['-p', '5353'])

        res = func(*args, **kwargs)

        server_.stop()

        return res

    return new_func

@server
def test_server():
    pass


def assert_is_valid_response(url: str, method_name: str = 'get', valid_status_code: int = 200):
    json_data = requester.get_json(url, method_name)
    assert isinstance(json_data, dict)

    request = requester.create_request(url, method_name)
    assert request.status_code == valid_status_code

@server
def test_main_page():
    assert_is_valid_response(main_page)

@server
def test_tracks():
    assert_is_valid_response(tracks_page)

@server
def test_track_detail():
    assert_is_valid_response(tracks_detail_page)
    tracks_data = requester.get_json(tracks_detail_page)

    assert 'name' in tracks_data
    assert 'artist' in tracks_data
    assert 'album' in tracks_data
