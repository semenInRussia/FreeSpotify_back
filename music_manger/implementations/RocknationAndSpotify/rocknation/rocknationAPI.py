from typing import Optional

from bs4 import BeautifulSoup

import my_request
from music_manger.core.exceptions import NotFoundAlbumException, NotFoundArtistException
from music_manger.implementations.RocknationAndSpotify.utils import delete_sound_quality

base_url = 'https://rocknation.su'


def get_link_on_artist(name: str) -> Optional[str]:
    soup = _get_soup_of_search_artist(name)

    return _get_artist_link_by_soup(soup)


def _get_soup_of_search_artist(name: str) -> BeautifulSoup:
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

    soup = my_request.get_bs('https://rocknation.su/mp3/searchresult/', 'post', headers=headers, data=data)

    return soup


def _get_artist_link_by_soup(soup: BeautifulSoup):
    elements = _find_artist_elements(soup)

    return _get_artist_link_by_elements(elements)


def _find_artist_elements(soup: BeautifulSoup):
    return soup.select(r"a[href^='/mp3/band']")


def _get_artist_link_by_elements(elements: list) -> str:
    try:
        element = elements[0]
    except IndexError:
        raise NotFoundArtistException
    else:
        link_for_rocknation = element.get('href')

        link = base_url + link_for_rocknation

        return link


class RocknationAlbums:
    def get_link_on_img(self, artist_name: str = None, album_name: str = None, link_on_album: str = None):
        """
        Get link on album image.
        You must take  (artist & album  name) or (link_on_album).
        """
        self._assert_is_valid_args_for_link_on_img(album_name, artist_name, link_on_album)

        if not link_on_album:
            link_on_album = self.get_link(artist_name, album_name)

        return self._get_link_on_img_by_album_link(link_on_album)

    @staticmethod
    def _assert_is_valid_args_for_link_on_img(album_name, artist_name, link_on_album):
        assert (artist_name and album_name) or link_on_album

    def _get_link_on_img_by_album_link(self, link: str):
        self._raise_not_found_error_if_should(link, 'artist')

        soup = my_request.get_bs(link)

        img = soup.select_one(f"img[src^='/upload/images/albums/']")
        src = img.get("src")

        self._raise_not_found_error_if_should(src, 'album')

        url = base_url + src
        return url

    def get_link(self, artist_name: str, album_name: str) -> Optional[str]:
        album_name = delete_sound_quality(album_name)
        artist_name = delete_sound_quality(artist_name)

        link_on_artist = get_link_on_artist(artist_name)

        return self._get_link_by_link_on_artist(link_on_artist, album_name)

    def _get_link_by_link_on_artist(self, link_on_artist: str, album_name: str):
        self._raise_not_found_error_if_should(link_on_artist, 'artist')

        soup = my_request.get_bs(link_on_artist)
        link_on_album = self._find_link_on_album_by_soup(soup, album_name)

        self._raise_not_found_error_if_should(link_on_album, 'album')

        return link_on_album

    def _find_link_on_album_by_soup(self, soup: BeautifulSoup, album_name: str) -> str:
        albums_links = self._find_links_on_album(soup)

        album_link = self._find_album_link(albums_links, album_name)

        self._raise_not_found_error_if_should(album_link, 'album')

        url_for_rocknation = album_link.get('href')

        url = base_url + url_for_rocknation

        return url

    @staticmethod
    def _is_not_valid_url(link: str):
        return not link

    @staticmethod
    def _find_album_link(albums_links: list, album_name: str):
        for albums_link in albums_links:
            if album_name.lower() in albums_link.text.lower():
                return albums_link

    @staticmethod
    def _try_delete_value_in_brackets(string: str) -> str:
        open_bracket = '('

        index_bracket = string.find(open_bracket)
        index_space_before_bracket = index_bracket - 1
        return string[:index_space_before_bracket]

    @staticmethod
    def _find_links_on_album(soup: BeautifulSoup) -> list:
        albums_elements = soup.select('a[href^="/mp3/album"]')

        return albums_elements

    def _raise_not_found_error_if_should(self, link: str, exception_type: str):
        if self._is_not_valid_url(link):
            if exception_type == 'artist':
                raise NotFoundArtistException
            elif exception_type == 'album':
                raise NotFoundAlbumException
            else:
                raise AttributeError(f'{exception_type} - is undefined exception type!')


class RocknationArtists:
    @staticmethod
    def get_link(artist_name: str):
        return get_link_on_artist(artist_name)

    def get_link_on_img(self, artist_name: str):
        link_on_artist = get_link_on_artist(artist_name)

        image = self._get_img_by_soup_by_url(link_on_artist)

        return base_url + image.get('src')

    def _get_img_by_soup_by_url(self, url: str):
        soup = my_request.get_bs(url)

        return self._get_img_by_soup(soup)

    def _get_img_by_soup(self, soup: BeautifulSoup):
        return soup.select_one('img[src^="/upload/images/bands"]')


class Rocknation:
    artists = RocknationArtists()
    albums = RocknationAlbums()
