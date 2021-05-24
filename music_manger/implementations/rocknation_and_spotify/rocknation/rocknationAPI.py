from typing import List
from typing import Optional

from bs4 import BeautifulSoup
from bs4 import Tag

from _low_level_utils import cashed_function
from music_manger.core.exceptions import NotFoundAlbumException
from music_manger.core.exceptions import NotFoundArtistException
from music_manger.core.exceptions import NotFoundTrackException
from brackets_lib import delete_all_values_with_all_brackets

from music_manger.music_manger import AbstractAlbums
from music_manger.music_manger import AbstractArtists
from music_manger.music_manger import AbstractMusicManager
from music_manger.music_manger import AbstractTracks
from music_manger.utils import delete_year_in_album_name
import my_request
import parsing_lib
from similarity_lib import is_similar_strings
from similarity_lib import search_string_similar_to

ROCKNATION_BASE_URL = 'http://rocknation.su'
ROCKNATION_BASE_UPLOAD_MP3_URL = ROCKNATION_BASE_URL + "/upload/mp3/"


def _raise_exception_if_is_false(obj, exception):
    if not obj:
        raise exception


class RocknationArtists(AbstractArtists):
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

        soup = parsing_lib.get_bs('https://rocknation.su/mp3/searchresult/', 'post', headers=headers, data=data)

        return soup

    def _get_artist_link_by_soup(self, soup: BeautifulSoup):
        elements = self._find_artist_elements(soup)

        link = parsing_lib.get_first_link_by_elements_or_raise_exception(
            elements,
            exception=NotFoundArtistException,
            base_url=ROCKNATION_BASE_URL
        )

        return link

    @staticmethod
    def _find_artist_elements(soup: BeautifulSoup):
        return soup.select(r"a[href^='/mp3/band']")

    @cashed_function
    def get_link_on_img(self, artist_name: str) -> str:
        link_on_artist = self.get_link(artist_name)
        link_on_image = self._get_link_on_img_by_link_on_artist(link_on_artist)

        return link_on_image

    @cashed_function
    def _get_link_on_img_by_link_on_artist(self, link_on_artist: str) -> str:
        element = parsing_lib.cashed_select_one_element_on_page(
            link_on_artist,
            'img[src^="/upload/images/bands"]'
        )

        return parsing_lib.get_absolute_url_by_element(element, ROCKNATION_BASE_URL, url_attribute_of_tag="src")


class RocknationAlbums(AbstractAlbums):
    @cashed_function
    def get_link_on_img(self, artist_name: str, album_name: str):
        link_on_album = self.get_link(artist_name, album_name)
        link_on_img = self._get_link_on_img_by_album_link(link_on_album)

        return link_on_img

    @staticmethod
    def _get_link_on_img_by_album_link(album_link: str):
        element = parsing_lib.cashed_select_one_element_on_page(album_link, f"img[src^='/upload/images/albums/']")

        _raise_exception_if_is_false(element, NotFoundAlbumException)

        link_on_img = parsing_lib.get_absolute_url_by_element(element, ROCKNATION_BASE_URL, url_attribute_of_tag="src")

        return link_on_img

    @cashed_function
    def get_link(self, artist_name: str, album_name: str) -> Optional[str]:
        album_name = delete_all_values_with_all_brackets(album_name)
        artist_name = delete_all_values_with_all_brackets(artist_name)

        link_on_artist = self._artists.get_link(artist_name)
        link_on_album = self._get_link_on_album_by_link_on_artist(link_on_artist, album_name)

        return link_on_album

    def _get_link_on_album_by_link_on_artist(self, link_on_artist: str, album_name: str) -> str:
        links = self._find_links_on_albums_elements_by_link_on_artist(link_on_artist)
        link = self._find_looking_link_on_album_element(links, album_name)

        _raise_exception_if_is_false(link, NotFoundAlbumException)

        url = parsing_lib.get_absolute_url_by_element(link, ROCKNATION_BASE_URL)

        return url

    @staticmethod
    def _find_links_on_albums_elements_by_link_on_artist(link_on_artist: str) -> List[Tag]:
        return parsing_lib.cashed_select_elements_on_page(
            link_on_artist,
            'a[href^="/mp3/album"]'
        )

    @staticmethod
    def _find_looking_link_on_album_element(links_elements: list, album_name: str) -> Optional[Tag]:
        for link_element in links_elements:
            actual_album_name = delete_year_in_album_name(link_element.text)

            if is_similar_strings(album_name, actual_album_name):
                return link_element

    @property
    def _artists(self):
        return RocknationArtists()


class RocknationTracks(AbstractTracks):
    @cashed_function
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
        pattern = ROCKNATION_BASE_UPLOAD_MP3_URL + '[^"]+'

        return parsing_lib.cashed_search_on_page(album_link, pattern)

    def _find_looking_link_on_track(self, links: List[str], track_name: str) -> str:
        tracks_names_and_normalized_links = dict(map(
            lambda link: (self._track_name_from_link(link), my_request.normalize_link(link)),
            links
        ))

        track_names = list(tracks_names_and_normalized_links.keys())

        actual_track_name = search_string_similar_to(track_name, track_names)

        if not is_similar_strings(actual_track_name, track_name):
            raise NotFoundTrackException

        return tracks_names_and_normalized_links[actual_track_name]

    @staticmethod
    def _track_name_from_link(link: str) -> str:
        """Return track name from current link.
        For example:
        >> _track_name_from_link(http://rocknation.su/upload/mp3/Nirvana/1993 -In Utero/11. Tourette's.mp3) == Tourette's
        """
        parts_of_link = link.split(".")
        track_name_with_start_space = parts_of_link[-2]
        track_name = track_name_with_start_space[1:]

        return track_name

    def get_link_on_img(self, artist_name: str, album_name: str, track_name: str) -> str:
        return self._albums.get_link_on_img(artist_name, album_name)

    @property
    def _albums(self):
        return RocknationAlbums()


class Rocknation(AbstractMusicManager):
    artists = RocknationArtists()
    albums = RocknationAlbums()
    tracks = RocknationTracks()
