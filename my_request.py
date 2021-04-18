import json
from typing import Dict, Callable

import requests
from bs4 import BeautifulSoup

dependencies_of_methods_on_name: Dict[str, Callable] = {
    "get": requests.get,
    "post": requests.post,
    "put": requests.put,
    "delete": requests.delete,
}


def get_bs(url: str, method_name: str = 'get', **kwargs) -> BeautifulSoup:
    html = get_content(url, method_name, **kwargs)

    return BeautifulSoup(html, "html.parser")


def get_json(url: str, method_name: str = 'get', **kwargs):
    return json.loads(get_content(url, method_name, **kwargs))


def get_content(url: str, method_name: str = 'get', **kwargs):
    return create_request(url, method_name, **kwargs).text


def create_request(url: str, method_name: str = 'get', **kwargs):
    method = get_method_by_name(method_name)

    return method(url, **kwargs)


def get_method_by_name(method_name: str = 'get') -> Callable:
    return dependencies_of_methods_on_name.get(method_name)
