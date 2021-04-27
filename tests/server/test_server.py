from collections import namedtuple

from flask.testing import FlaskClient
import pytest

from server import handlers

PageDetail = namedtuple("PageDetail", ["url", "required_fields_names"])


@pytest.fixture()
def client():
    handlers.app.config['TESTING'] = True

    with handlers.app.test_client() as client:
        yield client


def test_main_page(client: FlaskClient):
    assert client.get("/api", follow_redirects=True).status_code == 200


def test_welcome_pages(client: FlaskClient):
    welcome_pages_urls = [
        '/api/artists',
        '/api/albums',
        '/api/tracks'
    ]

    welcome_pages_response_status_codes = list(map(
        lambda url: client.get(url, follow_redirects=True).status_code,

        welcome_pages_urls
    ))

    for actual_url, status_code in zip(welcome_pages_urls, welcome_pages_response_status_codes):
        assert status_code == 200, "Status code of url '{}' isn't equal 200".format(actual_url)


# This is very long test on my computer: 1m 917ms...
# todo: make it quick!

def test_detail_pages(client: FlaskClient):
    detail_pages = [
        PageDetail('api/artists/detail/AC-DC', required_fields_names=["top", "albums", "name", "link", "link_on_img"]),

        PageDetail('api/albums/detail/AC-DC/Fly-on-The-Wall', required_fields_names=[
            "tracks", "artist", "name", "release_date", "link", "link_on_img"
        ]),

        PageDetail('api/tracks/detail/AC-DC/Flick-of-The-Switch/Rising-Power', required_fields_names=[
            "name", "artist", "album", "disc_number"
        ])
    ]

    get_json = lambda detail_page: client.get(detail_page.url, follow_redirects=True).json

    details_pages_jsons = list(map(
        get_json,
        detail_pages
    ))

    for actual_json, excepted_detail_page in zip(details_pages_jsons, detail_pages):
        for required_field in excepted_detail_page.required_fields_names:
            print(actual_json)
            assert required_field in actual_json, f"Json of {excepted_detail_page.url} must has {required_field}."
