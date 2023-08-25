import itertools
from collections.abc import Iterable
from typing import Optional

from bs4 import BeautifulSoup, Tag

from FreeSpotify_back import my_request, parsing_lib
from FreeSpotify_back._low_level_utils import cached_function
from FreeSpotify_back.music_manager import (
    AbstractAlbums,
    AbstractArtists,
    AbstractMusicManager,
    AbstractTracks,
)
from FreeSpotify_back.music_manager.core.exceptions import (
    NotFoundAlbumError,
    NotFoundArtistError,
    NotFoundTrackError,
)
from FreeSpotify_back.music_manager.utils import (
    delete_sound_quality,
    delete_year_in_album_name,
)
from FreeSpotify_back.similarity_lib import is_similar_strings, search_string_similar_to

ROCKNATION_BASE_URL = "http://rocknation.su"
ROCKNATION_BASE_UPLOAD_MP3_URL = ROCKNATION_BASE_URL + "/upload/mp3/"


class RocknationArtists(AbstractArtists):
    """Implementation of music manager (artist manager) for Rocknation."""

    @cached_function
    def get_link(self, artist_name: str) -> Optional[str]:  # noqa: D102
        artist_name = delete_sound_quality(artist_name)

        soup = self._get_soup_of_search_response(artist_name)
        return self._get_artist_link_by_soup(soup)

    @staticmethod
    @cached_function
    def _get_soup_of_search_response(name: str) -> BeautifulSoup:
        # code from https://curl.trillworks.com

        headers = {
            "authority": "rocknation.su",
            "cache-control": "max-age=0",
            "upgrade-insecure-requests": "1",
            "origin": "https://rocknation.su",
            "content-type": "application/x-www-form-urlencoded",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) "
            "AppleWebKit/537.36 (KHTML, like Gecko)"
            " Chrome/84.0.4147.105 Safari/537.36 OPR/70.0.3728.106",
            "accept": "text/html,application/"
            "xhtml+xml,application/"
            "xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "sec-fetch-site": "same-origin",
            "sec-fetch-mode": "navigate",
            "sec-fetch-user": "?1",
            "sec-fetch-dest": "document",
            "referer": "https://rocknation.su/mp3/",
            "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        }

        data = {
            "text_mp3": name,
            "enter_mp3": "Search",
        }

        return parsing_lib.get_bs(
            "https://rocknation.su/mp3/searchresult/",
            "post",
            headers=headers,
            data=data,
        )

    def _get_artist_link_by_soup(self, soup: BeautifulSoup) -> Optional[str]:
        elements = self._find_artist_elements(soup)

        return parsing_lib.get_first_link_by_elements_or_raise_exception(
            elements,
            exception=NotFoundArtistError,
            base_url=ROCKNATION_BASE_URL,
        )

    @staticmethod
    def _find_artist_elements(soup: BeautifulSoup) -> list[Tag]:
        return soup.select(r"a[href^='/mp3/band']")

    @cached_function
    def get_link_on_img(self, artist_name: str) -> str:  # noqa: D102
        link_on_artist = self.get_link(artist_name)
        return self._get_link_on_img_by_link_on_artist(link_on_artist)

    @cached_function
    def _get_link_on_img_by_link_on_artist(self, link_on_artist: str) -> str:
        element = parsing_lib.cached_select_one_element_on_page(
            link_on_artist,
            'img[src^="/upload/images/bands"]',
        )

        if element is None:
            raise NotFoundArtistError

        return parsing_lib.get_absolute_url_by_element(
            element, ROCKNATION_BASE_URL, url_attribute_of_tag="src"
        )


class RocknationAlbums(AbstractAlbums):
    """Implementation of music manager (albums manager) for Rocknation."""

    @cached_function
    def get_link_on_img(
        self, artist_name: str, album_name: str  # noqa: D102
    ) -> Optional[str]:
        link_on_album = self.get_link(artist_name, album_name)

        if link_on_album is None:
            return None

        return self._get_link_on_img_by_album_link(link_on_album)

    @staticmethod
    def _get_link_on_img_by_album_link(album_link: str) -> str:
        element = parsing_lib.cached_select_one_element_on_page(
            album_link, "img[src^='/upload/images/albums/']"
        )

        if element is None:
            raise NotFoundAlbumError

        return parsing_lib.get_absolute_url_by_element(
            element, ROCKNATION_BASE_URL, url_attribute_of_tag="src"
        )

    @cached_function
    def get_link(
        self, artist_name: str, album_name: str
    ) -> Optional[str]:  # noqa: D102, E501
        album_name = delete_sound_quality(album_name)

        link_on_artist = self._artists.get_link(artist_name)

        if link_on_artist is None:
            raise NotFoundAlbumError

        return self._find_album_link_on_artist_page(link_on_artist, album_name)

    def _find_album_link_on_artist_page(
        self, link_on_artist: str, album_name: str
    ) -> str:
        links = self._find_albums_links_elements_artist_page(link_on_artist)
        link_element = self._find_looking_link_on_album_element(links, album_name)

        if link_element is None:
            raise NotFoundAlbumError

        return parsing_lib.get_absolute_url_by_element(
            link_element, ROCKNATION_BASE_URL
        )

    def _find_albums_links_elements_artist_page(
        self, link_on_artist: str
    ) -> Iterable[Tag]:
        for page_link in self._all_artist_albums_pages_links(link_on_artist):
            links_on_page = self._all_albums_links_on_page(page_link)

            if not links_on_page:
                break

            yield from links_on_page

    @staticmethod
    def _all_artist_albums_pages_links(link_on_artist: str) -> Iterable[str]:
        yield link_on_artist
        for page_num in itertools.count(1):
            yield f"{link_on_artist}/{page_num}"

    @staticmethod
    def _all_albums_links_on_page(link_on_albums: str) -> Iterable[Tag]:
        return parsing_lib.cached_select_elements_on_page(
            link_on_albums, 'a[href^="/mp3/album"]'
        )

    def _find_looking_link_on_album_element(
        self, links_elements: Iterable[Tag], album_name: str
    ) -> Optional[Tag]:
        album_link = search_string_similar_to(
            album_name, links_elements, key=self._from_tag_to_link_on_album
        )
        actual_album_name = self._from_tag_to_link_on_album(album_link)

        if not is_similar_strings(actual_album_name, album_name):
            raise NotFoundAlbumError

        return album_link

    @staticmethod
    def _from_tag_to_link_on_album(tag: Tag) -> str:
        return delete_year_in_album_name(tag.text)

    @property
    def _artists(self) -> "RocknationArtists":
        return RocknationArtists()


class RocknationTracks(AbstractTracks):
    """Implementation of music manager (artist manager) for Rocknation."""

    @cached_function
    def get_link(
        self, artist_name: str, album_name: str, track_name: str  # noqa: D102
    ) -> str:
        link_on_album = self._albums.get_link(artist_name, album_name)
        link_on_track = self._find_link_on_track_on_album_page(
            link_on_album, track_name
        )

        return link_on_track  # noqa: RET504

    @cached_function
    def _find_link_on_track_on_album_page(
        self, link_on_album: str, track_name: str
    ) -> str:
        all_links_on_tracks = self._find_all_links_on_tracks_on_album_page(
            link_on_album
        )
        return self._find_looking_link_on_track(all_links_on_tracks, track_name)

    @staticmethod
    def _find_all_links_on_tracks_on_album_page(
        album_link: str,
    ) -> Iterable[str]:
        pattern = ROCKNATION_BASE_UPLOAD_MP3_URL + '[^"]+'

        return parsing_lib.cached_search_on_page(album_link, pattern)

    def _find_looking_link_on_track(self, links: Iterable[str], track_name: str) -> str:
        track_link = search_string_similar_to(
            track_name, links, key=self._track_name_from_link
        )
        actual_track_name = self._track_name_from_link(track_link)

        if not is_similar_strings(actual_track_name, track_name):
            raise NotFoundTrackError

        return my_request.normalize_link(track_link)

    @staticmethod
    def _track_name_from_link(link: str) -> str:
        parts_of_link = link.split(".")
        track_name_with_start_space = parts_of_link[-2]
        return track_name_with_start_space[1:]

    def get_link_on_img(
        self,  # noqa: D102
        artist_name: str,
        album_name: str,
        _: str,  # track_name
    ) -> Optional[str]:
        return self._albums.get_link_on_img(artist_name, album_name)

    @property
    def _albums(self) -> "RocknationAlbums":
        return RocknationAlbums()


class Rocknation(AbstractMusicManager):
    """Implementation of the music manager for rocknation."""

    artists = RocknationArtists()
    albums = RocknationAlbums()
    tracks = RocknationTracks()
