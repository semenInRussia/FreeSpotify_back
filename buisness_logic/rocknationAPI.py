from typing import Optional

import requests
from bs4 import BeautifulSoup
from loguru import logger

from buisness_logic.SpotifyWebAPI.features import Spotify
from buisness_logic.core.exceptions import NotFoundAlbumException, NotFoundArtistException

base_url = 'https://rocknation.su'
spotify = Spotify()

headers = {

}


def get_link_on_album_img(artist_name: str = None, album_name: str = None,
                          link_on_album: str = None):
    """
    Get link on album image,
    You have to give  (artist & album  name) or (link_on_album)
    :param artist_name: precise artist name
    :param album_name: precise album name
    :param link_on_album:
    :return: link on album image
    """
    logger.debug(f"(artist_name and album_name) = {(artist_name and album_name)}; link_on_album = {link_on_album}")
    assert (artist_name and album_name) or link_on_album, "You have to give  (artist & album  name) or (link_on_album)!"

    if not link_on_album:
        link_on_album = get_link_on_album(artist_name, album_name)

    logger.info(f"link_on_album = {link_on_album}")

    return _get_link_on_img_from_rocknation(link_on_album)


def get_link_on_artist_img():
    pass

def _get_link_on_img_from_rocknation(link: str):
    try:
        html = _get_html(link)
    except requests.exceptions.MissingSchema:
        raise NotFoundAlbumException

    soup = BeautifulSoup(html)

    img = soup.select_one("img[src^='/upload/images/albums/']")
    src = img.get("src")

    url = base_url + src

    return url


def get_link_on_artist(artist_name: str) -> str:
    return _get_rocknation_artist_link(artist_name)


def get_link_on_track(approximate_artist_name: str, approximate_track_name: str, approximate_album_name: str) -> str:
    return ""


def get_link_on_album(artist_name: str, album_name: str, raise_exception=True) -> Optional[str]:
    try:
        album_name = _delete_value_in_brackets(album_name)
    except AttributeError:
        return

    link_on_artist = get_link_on_artist(artist_name)

    html = _get_html(link_on_artist)
    link_on_album = _find_link_on_album(html, album_name)

    if link_on_album is None:
        if raise_exception:
            raise NotFoundAlbumException
        else:
            return

    return link_on_album


# ******************"public" ****************** #
def _get_html(url: str) -> str:
    request = requests.get(url)
    return request.text


# **************** get artist link ***************** #
def _post_on_rocknation_search(name: str) -> requests.request:
    # code from https://curl.trillworks.com

    headers = {
        'authority': 'rocknation.su',
        'cache-control': 'max-age=0',
        'upgrade-insecure-requests': '1',
        'origin': 'https://rocknation.su',
        'content-type': 'application/x-www-form-urlencoded',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36 OPR/70.0.3728.106',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'referer': 'https://rocknation.su/mp3/',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'cookie': '__cfduid=d948ccccc29373abc0006ed4b6835ff431598442433; PHPSESSID=8q0gsvqfkven6jeeff8c0gm567; __auc=1544f3a61742a97fca905e248a0; _ga=GA1.2.764445782.1598442438; _gid=GA1.2.2031556336.1598442438; _ym_uid=15984424381035837204; _ym_d=1598442438; _ym_isad=2; __asc=186e004317430bed0133c294919; _ym_visorc_44253949=w; _gat=1; MarketGidStorage=%7B%220%22%3A%7B%22svspr%22%3A%22https%3A%2F%2Fwww.google.com%2F%22%2C%22svsds%22%3A39%2C%22TejndEEDj%22%3A%22Pgqv4HmuV%22%7D%2C%22C969731%22%3A%7B%22page%22%3A2%2C%22time%22%3A1598546912396%7D%2C%22C754836%22%3A%7B%22page%22%3A2%2C%22time%22%3A1598546913062%7D%7D',
    }

    data = {
        'text_mp3': name,
        'enter_mp3': 'Search'
    }

    response = requests.post('https://rocknation.su/mp3/searchresult/', headers=headers, data=data)
    return response


def _get_html_search_artist(name: str) -> str:
    request = _post_on_rocknation_search(name)

    return request.text


def _find_artist_elements(html: str):
    bs = BeautifulSoup(html, features="html.parser")

    selector_on_link_to_artist = r"a[href^='/mp3/band']"
    elements_for_rocknation = bs.select(selector_on_link_to_artist)

    return elements_for_rocknation


def _get_rocknation_artist_link_by_html(html: str) -> str:
    try:
        element = _find_artist_elements(html)[0]
    except IndexError:
        raise NotFoundArtistException
    link_for_rocknation = element.get('href')

    link = base_url + link_for_rocknation

    return link


# **************** get album ***************
def _find_link_on_album(html: str, album_name: str) -> str:
    albums_links = _find_links_on_album(html)
    for album_link in albums_links:
        if album_name.lower() in album_link.text.lower():
            url_for_rocknation = album_link.get('href')
            url = base_url + url_for_rocknation

            return url


def _delete_value_in_brackets(string: str) -> str:
    open_bracket = '('

    index_bracket = string.find(open_bracket)
    index_space_before_bracket = index_bracket - 1
    return string[:index_space_before_bracket]


def _find_links_on_album(html: str) -> list:
    """
    Find html tag with href on album from html.
    :param html: artist sites html
    :param album_name: album name
    :return: link on album
    """
    bs = BeautifulSoup(html, "html.parser")
    albums_elements = bs.select('a[href^="/mp3/album"]')

    return albums_elements


def _get_rocknation_artist_link(name):
    html = _get_html_search_artist(name)
    return _get_rocknation_artist_link_by_html(html)
