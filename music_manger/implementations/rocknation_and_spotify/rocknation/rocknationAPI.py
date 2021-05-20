from typing import List
from typing import Optional

from bs4 import BeautifulSoup

from _low_level_utils import cashed_function
from music_manger.core.exceptions import NotFoundAlbumException
from music_manger.core.exceptions import NotFoundArtistException
from music_manger.core.exceptions import NotFoundTrackException
from music_manger.implementations.rocknation_and_spotify.utils import delete_sound_quality
from music_manger.implementations.rocknation_and_spotify.utils import delete_year_in_album_name
from music_manger.music_manger import AbstractAlbums
from music_manger.music_manger import AbstractArtists
from music_manger.music_manger import AbstractMusicManager
from music_manger.music_manger import AbstractTracks
import my_request
from similarity_lib import is_similar_strings
from similarity_lib import search_string_similar_to

ROCKNATION_BASE_URL = 'https://rocknation.su'
ROCKNATION_BASE_UPLOAD_MP3_URL = ROCKNATION_BASE_URL + "/upload/mp3/"

RATIO_OF_SIMILARITY_TRACK_NAME_AND_URL = 0.18


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


class RocknationArtists(AbstractArtists):
    @cashed_function
    def get_link(self, artist_name: str) -> Optional[str]:
        soup = self._get_soup_of_search_response(artist_name)
        link = self._get_artist_link_by_soup(soup)

        _raise_exception_if_should(link, NotFoundArtistException)

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

        link = my_request.get_first_link_by_elements_or_raise_exception(
            elements,
            exception=NotFoundArtistException,
            base_url=ROCKNATION_BASE_URL
        )

        return link

    @staticmethod
    def _find_artist_elements(soup: BeautifulSoup):
        return soup.select(r"a[href^='/mp3/band']")

    @cashed_function
    def get_link_on_img(self, artist_name: str):
        link_on_artist = self.get_link(artist_name)
        image = self._get_link_on_img_by_link_on_artist(link_on_artist)

        return ROCKNATION_BASE_URL + image.get('src')

    @cashed_function
    def _get_link_on_img_by_link_on_artist(self, link_on_artist: str):
        return my_request.select_one_element_on_page(
            link_on_artist,
            'img[src^="/upload/images/bands"]'
        )


class RocknationAlbums(AbstractAlbums):
    @cashed_function
    def get_link_on_img(self, artist_name: str, album_name: str):
        link_on_album = self.get_link(artist_name, album_name)

        return self._get_link_on_img_by_album_link(link_on_album)

    @staticmethod
    def _get_link_on_img_by_album_link(album_link: str):
        _raise_exception_if_should(album_link, NotFoundAlbumException)

        img = my_request.select_one_element_on_page(album_link, f"img[src^='/upload/images/albums/']")
        src = img.get("src")

        _raise_exception_if_should(src, NotFoundAlbumException)

        url = ROCKNATION_BASE_URL + src

        return url

    @cashed_function
    def get_link(self, artist_name: str, album_name: str) -> Optional[str]:
        album_name = delete_sound_quality(album_name)
        artist_name = delete_sound_quality(artist_name)

        link_on_artist = self._artists.get_link(artist_name)
        link_on_album = self._get_link_on_album_by_link_on_artist(link_on_artist, album_name)

        return link_on_album

    def _get_link_on_album_by_link_on_artist(self, link_on_artist: str, album_name: str):
        links = self._find_links_on_albums_by_link_on_artist(link_on_artist)
        link = self._find_looking_link_on_album(links, album_name)

        _raise_exception_if_should(link, NotFoundAlbumException)

        url = my_request.get_absolute_url_by_element(link, ROCKNATION_BASE_URL)

        return url

    @staticmethod
    def _find_links_on_albums_by_link_on_artist(link_on_artist: str):
        return my_request.select_elements_on_page(
            link_on_artist,
            'a[href^="/mp3/album"]'
        )

    @staticmethod
    def _find_looking_link_on_album(links: list, album_name: str):
        for albums_link in links:
            actual_album_name = delete_year_in_album_name(albums_link.text)

            if is_similar_strings(album_name, actual_album_name):
                return albums_link

    @property
    def _artists(self):
        return RocknationArtists()


class RocknationTracks(AbstractTracks):
    def get_link(self, artist_name: str, album_name: str, track_name: str) -> str:
        link_on_album = self._albums.get_link(artist_name, album_name)
        link_on_track = self._find_link_on_track_on_album_page(link_on_album, track_name)

        return link_on_track

    def _find_link_on_track_on_album_page(self, link_on_album: str, track_name: str) -> str:
        all_links_on_tracks = self._find_all_links_on_tracks_on_album_page(link_on_album)
        link_on_track = self._find_looking_link_on_track(all_links_on_tracks, track_name)

        return link_on_track

    @staticmethod
    def _find_all_links_on_tracks_on_album_page(album_link: str) -> List[str]:
        pattern = 'http://rocknation.su/upload/mp3/[^"]+'

        return my_request.search_on_page(album_link, pattern)

    @staticmethod
    def _find_looking_link_on_track(links: List[str], track_name: str) -> str:
        # todo: Work for single tracks. For example: Back In Black (track) for Back In Black (album)
        actual_link_on_track = search_string_similar_to(track_name, links)

        if is_similar_strings(actual_link_on_track, track_name, RATIO_OF_SIMILARITY_TRACK_NAME_AND_URL):
            return actual_link_on_track

        else:
            raise NotFoundTrackException

    def get_link_on_img(self, artist_name: str, album_name: str, track_name: str) -> str:
        return self._albums.get_link_on_img(artist_name, album_name)

    @property
    def _albums(self):
        return RocknationAlbums()


class Rocknation(AbstractMusicManager):
    artists = RocknationArtists()
    albums = RocknationAlbums()
    tracks = RocknationTracks()
