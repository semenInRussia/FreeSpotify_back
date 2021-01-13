import json

import requests
from bs4 import BeautifulSoup


def get_bs(url: str, method_name: str = "get", **kwargs) -> BeautifulSoup:
    html = get_content(url, method_name, **kwargs)

    return BeautifulSoup(html, "html.parser")


def get_json(url: str, method_name: str = 'get'):
    return json.loads(get_content(url, method_name))


def get_content(url: str, method_name: str = 'get', **kwargs):
    return create_request(url, method_name, **kwargs).text


def create_request(url: str, method_name: str = 'get', **kwargs):
    return requests.request(method_name, url, **kwargs)
