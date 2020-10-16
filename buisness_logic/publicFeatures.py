from loguru import logger

from buisness_logic.SpotifyWebAPI.features import Spotify
from buisness_logic.rocknationAPI import get_link_on_album, get_link_on_artist, get_link_on_album_img, \
    _get_link_on_img_from_rocknation
from buisness_logic.spotifyPythonAPI import get_top_music_info_by_approximate_artist_title, \
    get_artist_info


_spotify = Spotify()

def get_tracks_top(artist_name, spotify: Spotify) -> list:
    tracks_info = get_top_music_info_by_approximate_artist_title(artist_name, spotify=spotify)

    logger.debug(f"tracks_info = {tracks_info}")

    cash = {
        'links_on_album': {},
        'links_on_album_img': {}
    }

    link_on_artist = get_link_on_artist(artist_name)

    for track in tracks_info:
        album_name = track['album_name']

        # get link on album
        link_on_album = _get_value_from_cash(cash['links_on_album'], key=album_name,
                                             get_default_value=lambda key: get_link_on_album(artist_name,
                                                                                             album_name,
                                                                                             raise_exception=False))
        logger.debug(f"link_on_album = {link_on_album}")

        def get_default_value(key):
            try:
                return get_link_on_album_img(link_on_album=link_on_album)
            except AssertionError:
                return None

        link_on_album_img = _get_value_from_cash(cash['links_on_album_img'], key=album_name,
                                                 get_default_value=get_default_value)

        # update data
        track["album_link"] = link_on_album
        track["artist_link"] = link_on_artist
        track["album_img_link"] = link_on_album_img

    return tracks_info


def _get_value_from_cash(cash: dict, key: str, get_default_value):
    """
    Get value from cash
    :param cash:
    :param key: key from cash
    :param get_default_value: is function (key) -> default value
    :return:
    """
    if not (key in cash):
        cash[key] = get_default_value(key)
    return cash[key]


def get_link_on_artist_img(spotify: Spotify, artist_name: str = None, artist_link: str = None):
    """(TAKE artist_name or artist_link)"""
    assert artist_name or artist_link

    if artist_name:
        artist_name = get_artist_info(artist_name, spotify)["name"]
        artist_link = get_link_on_artist(artist_name)

    return _get_link_on_img_from_rocknation(artist_link)
