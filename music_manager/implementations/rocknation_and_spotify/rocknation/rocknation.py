from typing import List
from typing import Optional

from bs4 import BeautifulSoup
from bs4 import Tag

from FreeSpotify_back._low_level_utils import cached_function

from FreeSpotify_back.similarity_lib import is_similar_strings
from FreeSpotify_back.similarity_lib import search_string_similar_to

from FreeSpotify_back import my_request
from FreeSpotify_back import parsing_lib

from ....core.exceptions import NotFoundAlbumException
from ....core.exceptions import NotFoundArtistException
from ....core.exceptions import NotFoundTrackException
from .... import AbstractAlbums
from .... import AbstractArtists
from .... import AbstractMusicManager
from .... import AbstractTracks
from ....utils import delete_sound_quality
from ....utils import delete_year_in_album_name

ROCKNATION_BASE_URL = 'http://rocknation.su'
ROCKNATION_BASE_UPLOAD_MP3_URL = ROCKNATION_BASE_URL + "/upload/mp3/"

max_albums_page_num = 100


def _raise_exception_if_is_false(obj, exception):
    if not obj:
        raise exception


class RocknationArtists(AbstractArtists):
    @cached_function
    def get_link(self, artist_name: str) -> Optional[str]:
        artist_name = delete_sound_quality(artist_name)

        soup = self._get_soup_of_search_response(artist_name)
        link = self._get_artist_link_by_soup(soup)

        return link

    @staticmethod
    @cached_function
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

        soup = parsing_lib.get_bs(
            'https://rocknation.su/mp3/searchresult/',
            'post',
            headers=headers,
            data=data
        )

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

    @cached_function
    def get_link_on_img(self, artist_name: str) -> str:
        link_on_artist = self.get_link(artist_name)
        link_on_image = self._get_link_on_img_by_link_on_artist(link_on_artist)

        return link_on_image

    @cached_function
    def _get_link_on_img_by_link_on_artist(self, link_on_artist: str) -> str:
        element = parsing_lib.cached_select_one_element_on_page(
            link_on_artist,
            'img[src^="/upload/images/bands"]'
        )

        return parsing_lib.get_absolute_url_by_element(element, ROCKNATION_BASE_URL, url_attribute_of_tag="src")


class RocknationAlbums(AbstractAlbums):
    @cached_function
    def get_link_on_img(self, artist_name: str, album_name: str):
        link_on_album = self.get_link(artist_name, album_name)
        link_on_img = self._get_link_on_img_by_album_link(link_on_album)

        return link_on_img

    @staticmethod
    def _get_link_on_img_by_album_link(album_link: str):
        element = parsing_lib.cached_select_one_element_on_page(album_link, "img[src^='/upload/images/albums/']")

        _raise_exception_if_is_false(element, NotFoundAlbumException)

        link_on_img = parsing_lib.get_absolute_url_by_element(element, ROCKNATION_BASE_URL, url_attribute_of_tag="src")

        return link_on_img

    @cached_function
    def get_link(self, artist_name: str, album_name: str) -> Optional[str]:
        album_name = delete_sound_quality(album_name)

        link_on_artist = self._artists.get_link(artist_name)
        link_on_album = self._get_link_on_album_by_link_on_artist(link_on_artist, album_name)

        return link_on_album

    def _get_link_on_album_by_link_on_artist(self, link_on_artist: str, album_name: str) -> str:
        links = self._find_links_on_albums_elements_by_link_on_artist(link_on_artist)
        link_element = self._find_looking_link_on_album_element(links, album_name)

        _raise_exception_if_is_false(link_element, NotFoundAlbumException)

        url = parsing_lib.get_absolute_url_by_element(link_element, ROCKNATION_BASE_URL)

        return url

    def _find_links_on_albums_elements_by_link_on_artist(self, link_on_artist: str) -> List[Tag]:
        for link_on_albums in self._get_all_albums_links(link_on_artist):
            new_links = self._find_links_on_albums_elements_on_one_albums_link(link_on_albums)

            yield from new_links

            if not new_links:
                break

    @staticmethod
    def _get_all_albums_links(link_on_artist: str) -> iter:
        current_page_albums_index = 0
        current_albums_link = link_on_artist

        while True:
            yield current_albums_link

            if my_request.is_not_valid_page(current_albums_link):
                return

            current_page_albums_index += 1
            current_albums_link = f"{link_on_artist}/{current_page_albums_index}"

    @staticmethod
    def _find_links_on_albums_elements_on_one_albums_link(link_on_albums: str) -> List[Tag]:
        return parsing_lib.cached_select_elements_on_page(
            link_on_albums,
            'a[href^="/mp3/album"]'
        )

    @staticmethod
    def _find_looking_link_on_album_element(links_elements: list, album_name: str) -> Optional[Tag]:
        album_names = map(
            lambda el: delete_year_in_album_name(el.text),
            links_elements
        )

        actual_album_name = search_string_similar_to(album_name, album_names)

        if not is_similar_strings(actual_album_name, album_name):
            raise NotFoundAlbumException

        return actual_link_element

    @property
    def _artists(self):
        return RocknationArtists()


class RocknationTracks(AbstractTracks):
    @cached_function
    @cached_function
    def get_link(self, artist_name: str, album_name: str, track_name: str) -> str:
        link_on_album = self._albums.get_link(artist_name, album_name)
        link_on_track = self._find_link_on_track_on_album_page(link_on_album, track_name)

        return link_on_track

    @cached_function
    def _find_link_on_track_on_album_page(self, link_on_album: str, track_name: str) -> str:
        all_links_on_tracks = self._find_all_links_on_tracks_on_album_page(link_on_album)
        link_on_track = self._find_looking_link_on_track(all_links_on_tracks, track_name)

        return link_on_track

    @staticmethod
    def _find_all_links_on_tracks_on_album_page(album_link: str) -> List[str]:
        pattern = ROCKNATION_BASE_UPLOAD_MP3_URL + '[^"]+'

        return parsing_lib.cached_search_on_page(album_link, pattern)

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
        parts_of_link = link.split(".")
        track_name_with_start_space = parts_of_link[-2]
        track_name = track_name_with_start_space[1:]

        return track_name

    def get_link_on_img(
            self,
            artist_name: str,
            album_name: str,
            _: str                        # track_name
    ) -> str:
        return self._albums.get_link_on_img(artist_name, album_name)

    @property
    def _albums(self):
        return RocknationAlbums()


class Rocknation(AbstractMusicManager):
    artists = RocknationArtists
    albums = RocknationAlbums
    tracks = RocknationTracks
