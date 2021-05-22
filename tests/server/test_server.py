from collections import namedtuple
from typing import List

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


@pytest.mark.parametrize(
    "url,required_fields_names",
    [
        ("api/artists/detail/AC-DC", ["top", "albums", "name", "link", "link_on_img"]),
        ("api/albums/detail/AC-DC/Fly-on-The-Wall", ["release_date", "tracks", "name", "link", "link_on_img"]),
        ("api/tracks/detail/AC-DC/Flick-of-The-Switch/Rising-Power", ["name", "artist", "album", "disc_number", "link"])
    ]
)
def test_detail_pages(client: FlaskClient, url: str, required_fields_names: List[str]):
    current_json = client.get(url, follow_redirects=True).json

    for required_field_name in required_fields_names:
        assert required_field_name in current_json, f"Json of {url} must has {required_field_name}."
