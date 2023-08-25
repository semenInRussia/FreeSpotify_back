import re
from typing import Optional

from bs4 import Tag

from ._low_level_utils import cached_function
from .my_request import (
    cached_get_bs,
    cached_get_content,
    get_absolute_url,
    get_bs,
    get_content,
)


def select_one_element_on_page(
    url: str, css_selector: str, method_name: str = "get", **kwargs
) -> Optional[Tag]:
    soup = get_bs(url, method_name, **kwargs)
    return soup.select_one(css_selector)


def select_elements_on_page(
    url: str, css_selector: str, method_name: str = "get", **kwargs
) -> list[Tag]:
    soup = get_bs(url, method_name, **kwargs)

    return soup.select(css_selector)


@cached_function
def cached_select_elements_on_page(
    url: str, css_selector: str, method_name: str = "get", **kwargs
) -> list[Tag]:
    soup = cached_get_bs(url, method_name, **kwargs)

    return soup.select(css_selector)


def cached_select_one_element_on_page(
    url: str, css_selector: str, method_name: str = "get", **kwargs
):
    soup = cached_get_bs(url, method_name, **kwargs)

    return soup.select_one(css_selector)


def get_first_link_by_elements_or_raise_exception(
    elements: list[Tag],
    exception: type[Exception],
    base_url: str,
    url_attribute_of_tag: str = "href",
) -> str:
    try:
        element = elements[0]
    except IndexError as exc:
        raise exception from exc
    else:
        return get_absolute_url_by_element(element, base_url, url_attribute_of_tag)


def get_absolute_url_by_element(
    element: Tag, base_url: str, url_attribute_of_tag: str = "href"
) -> str:
    relative_link = element.get(url_attribute_of_tag)

    if isinstance(relative_link, list) or relative_link is None:
        raise TypeError("Attribute of a tag should be plain string")

    return get_absolute_url(relative_link, base_url)


def search_on_page(url: str, pattern: str, method: str = "get", **kwargs) -> list[str]:
    string = get_content(url, method, **kwargs)
    return re.findall(pattern, string)


@cached_function
def cached_search_on_page(
    url: str, pattern: str, method: str = "get", **kwargs
) -> list[str]:
    string = cached_get_content(url, method, **kwargs)

    return re.findall(pattern, string)
