from typing import Optional

from bs4 import BeautifulSoup

from _low_level_utils import cashed_function
from music_manger.core.exceptions import NotFoundAlbumException
from music_manger.core.exceptions import NotFoundArtistException
from music_manger.implementations.rocknation_and_spotify.utils import delete_sound_quality

import my_request

base_url = 'https://rocknation.su'


def _is_not_valid_url(link: str):
    return not link


def _raise_exception_if_should(link: str, exception):
    """
    If link isn't corrent, raise exception.

    :param link:
    :type link str:

    :param exception:
    :type NotFoundArtistException | NotFoundAlbumException
    """
    if _is_not_valid_url(link):
        raise exception


class RocknationArtists:
    @cashed_function
    def get_link(self, artist_name: str) -> Optional[str]:
        soup = self._get_soup_of_search_response(artist_name)
        link = self._get_artist_link_by_soup(soup)

        return link

    @staticmethod
    def _get_soup_of_search_response(name: str) -> BeautifulSoup:
        # code from https://curl.trillworks.com

        headers = {
            'authority': 'rocknation.su',
            'cache-control': 'max-age=0',
            'upgrade-insecure-requests': '1',
            'origin': 'https://rocknation.su',
            'content-type': 'application/x-www-form-urlencoded',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko)'
                          ' Chrome/84.0.4147.105 Safari/537.36 OPR/70.0.3728.106',
            'accept': 'text/html,application/'
                      'xhtml+xml,application/'
                      'xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
            'referer': 'https://rocknation.su/mp3/',
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        }

        data = {
            'text_mp3': name,
            'enter_mp3': 'Search'
        }

        soup = my_request.get_bs('https://rocknation.su/mp3/searchresult/', 'post', headers=headers, data=data)

        return soup

    def _get_artist_link_by_soup(self, soup: BeautifulSoup):
        elements = self._find_artist_elements(soup)
        link = self._get_artist_link_by_elements(elements)

        return link

    @staticmethod
    def _find_artist_elements(soup: BeautifulSoup):
        return soup.select(r"a[href^='/mp3/band']")

    @staticmethod
    def _get_artist_link_by_elements(elements: list) -> str:
        try:
            element = elements[0]
        except IndexError:
            raise NotFoundArtistException
        else:
            link_for_rocknation = element.get('href')

            link = base_url + link_for_rocknation

            return link

    @cashed_function
    def get_link_on_img(self, artist_name: str):
        link_on_artist = self.get_link(artist_name)
        image = self._get_img_by_url(link_on_artist)

        return base_url + image.get('src')

    @cashed_function
    def _get_img_by_url(self, url: str):
        soup = my_request.get_bs(url)

        return self._get_img_by_soup(soup)

    @staticmethod
    def _get_img_by_soup(soup: BeautifulSoup):
        return soup.select_one('img[src^="/upload/images/bands"]')


class RocknationAlbums:
    @cashed_function
    def get_link_on_img(self, artist_name: str, album_name: str):
        link_on_album = self.get_link(artist_name, album_name)

        return self._get_link_on_img_by_album_link(link_on_album)

    @staticmethod
    def _get_link_on_img_by_album_link(album_link: str):
        _raise_exception_if_should(album_link, NotFoundAlbumException)

        soup = my_request.get_bs(album_link)

        img = soup.select_one(f"img[src^='/upload/images/albums/']")
        src = img.get("src")

        _raise_exception_if_should(src, NotFoundAlbumException)

        url = base_url + src

        return url

    @cashed_function
    def get_link(self, artist_name: str, album_name: str) -> Optional[str]:
        album_name = delete_sound_quality(album_name)
        artist_name = delete_sound_quality(artist_name)

        link_on_artist = self._artists.get_link(artist_name)

        _raise_exception_if_should(link_on_artist, NotFoundArtistException)

        return self._get_link_by_link_on_artist(link_on_artist, album_name)

    @cashed_function
    def _get_link_by_link_on_artist(self, link_on_artist: str, album_name: str):
        _raise_exception_if_should(link_on_artist, NotFoundArtistException)

        soup = my_request.get_bs(link_on_artist)
        link_on_album = self._find_link_on_album_by_soup(soup, album_name)

        _raise_exception_if_should(link_on_album, NotFoundAlbumException)

        return link_on_album

    def _find_link_on_album_by_soup(self, soup: BeautifulSoup, album_name: str) -> str:
        albums_links = self._find_links_on_album(soup)
        album_link = self._find_album_link_in_link(albums_links, album_name)

        _raise_exception_if_should(album_link, NotFoundAlbumException)

        url_for_rocknation = album_link.get('href')
        url = base_url + url_for_rocknation

        return url

    @staticmethod
    def _find_links_on_album(soup: BeautifulSoup) -> list:
        albums_elements = soup.select('a[href^="/mp3/album"]')

        return albums_elements

    @staticmethod
    def _find_album_link_in_link(albums_links: list, album_name: str):
        for albums_link in albums_links:
            if album_name.lower() in albums_link.text.lower():
                return albums_link

    @property
    def _artists(self):
        return RocknationArtists()


class Rocknation:
    artists = RocknationArtists()
    albums = RocknationAlbums()
