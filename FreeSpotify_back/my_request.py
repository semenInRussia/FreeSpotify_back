import json
from collections.abc import Callable
from json import JSONDecodeError

import requests
from bs4 import BeautifulSoup

from ._low_level_utils import cached_function
from .core.exceptions import NotJsonResponseFromUrl

dependencies_of_methods_on_name: dict[str, Callable] = {
    "get": requests.get,
    "post": requests.post,
    "put": requests.put,
    "delete": requests.delete,
}


def humanized_link(link: str) -> str:
    return link.replace("%20", " ")


def normalize_link(link: str) -> str:
    return link.replace(" ", "%20")


def get_absolute_url(relative_url: str, base_url: str) -> str:
    return base_url + relative_url


def get_bs(url: str, method_name: str = 'get', **kwargs) -> BeautifulSoup:
    html = get_content(url, method_name, **kwargs)

    return BeautifulSoup(html, "html.parser")


cached_get_bs = cached_function(get_bs)


def get_json(url: str, method_name: str = 'get', **kwargs) -> dict:
    content = get_content(url, method_name, **kwargs)
    return _try_load_content_to_json(content, url)


def _try_load_content_to_json(content_of_page: str, url: str) -> dict:
    try:
        return json.loads(content_of_page)
    except JSONDecodeError as exc:
        raise NotJsonResponseFromUrl(url) from exc


def get_content(url: str, method_name: str = 'get', **kwargs) -> str:
    return create_request(url, method_name, **kwargs).text


cached_get_content = cached_function(get_content)


def is_not_valid_page(link_on_page: str, method: str = 'get', **kwargs) -> bool:
    try:
        create_request(link_on_page, method_name=method, **kwargs)
    except requests.exceptions.ConnectionError:
        return True
    else:
        return False


def create_request(url: str, method_name: str = 'get', **kwargs):
    method = get_method_by_name(method_name)
    return method(url, **kwargs)


def get_method_by_name(method_name: str = 'get') -> Callable:
    return dependencies_of_methods_on_name[method_name]
