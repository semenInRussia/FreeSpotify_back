import json
from json import JSONDecodeError
import re
from typing import Callable
from typing import Dict
from typing import List

from bs4 import BeautifulSoup
from bs4 import Tag
import requests

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


def select_one_element_on_page(url: str, css_selector: str, method_name='get', **kwargs) -> Tag:
    soup = get_bs(url, method_name, **kwargs)

    return soup.select_one(css_selector)


def select_elements_on_page(
        url: str, css_selector: str,
        method_name='get',
        **kwargs
) -> List[Tag]:
    soup = get_bs(url, method_name, **kwargs)

    return soup.select(css_selector)


def get_first_link_by_elements_or_raise_exception(
        elements: List[Tag],
        exception,
        base_url: str,
        url_attribute_of_tag: str = 'href'
) -> str:
    try:
        element = elements[0]
    except IndexError:
        raise exception
    else:
        return get_absolute_url_by_element(element, base_url, url_attribute_of_tag)


def get_absolute_url_by_element(element: Tag, base_url: str, url_attribute_of_tag: str = 'href') -> str:
    relative_link = element.get(url_attribute_of_tag)
    absolute_link = base_url + relative_link

    return absolute_link


def search_on_page(url: str, pattern: str, method: str = 'get', **kwargs) -> List[str]:
    string = get_content(url, method, **kwargs)

    return re.findall(pattern, string)


def get_bs(url: str, method_name: str = 'get', **kwargs) -> BeautifulSoup:
    html = get_content(url, method_name, **kwargs)

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


def create_request(url: str, method_name: str = 'get', **kwargs):
    method = get_method_by_name(method_name)

    return method(url, **kwargs)


def get_method_by_name(method_name: str = 'get') -> Callable:
    return dependencies_of_methods_on_name.get(method_name)
