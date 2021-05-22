import json
from json import JSONDecodeError
from typing import Callable
from typing import Dict

from bs4 import BeautifulSoup
import requests

from _low_level_utils import cashed_function
from core.exceptions import NotJsonResponseFromUrl

dependencies_of_methods_on_name: Dict[str, Callable] = {
    "get": requests.get,
    "post": requests.post,
    "put": requests.put,
    "delete": requests.delete
}


def humanized_link(link: str) -> str:
    link = link.replace("%20", " ")

    return link


def normalize_link(link: str) -> str:
    link = link.replace(" ", "%20")

    return link


def get_absolute_url(relative_url: str, base_url: str) -> str:
    return base_url + relative_url


def get_bs(url: str, method_name: str = 'get', **kwargs) -> BeautifulSoup:
    html = get_content(url, method_name, **kwargs)

    return BeautifulSoup(html, "html.parser")


def cashed_get_bs(url: str, method_name: str = 'get', **kwargs) -> BeautifulSoup:
    html = cashed_get_content(url, method_name, **kwargs)

    return BeautifulSoup(html, "html.parser")


def get_json(url: str, method_name: str = 'get', **kwargs):
    content = get_content(url, method_name, **kwargs)
    json_data = _try_load_content_to_json(content, url)

    return json_data


def _try_load_content_to_json(content_of_page: str, url: str):
    try:
        return json.loads(content_of_page)
    except JSONDecodeError:
        raise NotJsonResponseFromUrl(url)


def get_content(url: str, method_name: str = 'get', **kwargs):
    return create_request(url, method_name, **kwargs).text


cashed_get_content = cashed_function(get_content)


def create_request(url: str, method_name: str = 'get', **kwargs):
    method = get_method_by_name(method_name)

    return method(url, **kwargs)


def get_method_by_name(method_name: str = 'get') -> Callable:
    return dependencies_of_methods_on_name.get(method_name)
