import re
from typing import List

from bs4 import Tag

from my_request import cashed_get_bs
from my_request import cashed_get_content
from my_request import get_absolute_url
from my_request import get_bs
from my_request import get_content


def select_one_element_on_page(url: str, css_selector: str, method_name='get', **kwargs) -> Tag:
    soup = get_bs(url, method_name, **kwargs)

    return soup.select_one(css_selector)


def select_elements_on_page(
        url: str,
        css_selector: str,
        method_name='get',
        **kwargs
) -> List[Tag]:
    soup = get_bs(url, method_name, **kwargs)

    return soup.select(css_selector)


def cashed_select_elements_on_page(
        url: str,
        css_selector: str,
        method_name='get',
        **kwargs
) -> List[Tag]:
    soup = cashed_get_bs(url, method_name, **kwargs)

    return soup.select(css_selector)


def cashed_select_one_element_on_page(url: str, css_selector: str, method_name='get', **kwargs):
    soup = cashed_get_bs(url, method_name, **kwargs)

    return soup.select_one(css_selector)


def get_first_link_by_elements_or_raise_exception(
        elements: List[Tag],
        exception,
        base_url: str,
        url_attribute_of_tag: str = 'href'
) -> str:
    try:
        element = elements[0]
    except IndexError as exc:
        raise exception from exc
    else:
        return get_absolute_url_by_element(element, base_url, url_attribute_of_tag)


def get_absolute_url_by_element(element: Tag, base_url: str,
                                url_attribute_of_tag: str = 'href') -> str:
    relative_link = element.get(url_attribute_of_tag)

    return get_absolute_url(relative_link, base_url)


def search_on_page(url: str, pattern: str, method: str = 'get', **kwargs) -> List[str]:
    string = get_content(url, method, **kwargs)

    return re.findall(pattern, string)


def cashed_search_on_page(url: str, pattern: str, method: str = 'get', **kwargs) -> List[str]:
    string = cashed_get_content(url, method, **kwargs)

    return re.findall(pattern, string)
